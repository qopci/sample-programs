import pytest

from test.fixtures import sources, docker_client
from test.project import ProjectType

sorting_invalid_permutations = (
    'description,in_params,expected', [
        (
            'no input',
            None,
            'Usage: please input a number'
        ), (
            'empty input',
            '""',
            'Usage: please input a number'
        ), (
            'invalid input: not a number',
            '"a"',
            'Usage: please input a number'
        )
    ]
)

sorting_valid_permutations = (
    'description,in_params,expected', [
        (
            'sample input: even',
            '2',
            'Even'
        ), (
            'sample input: odd',
            '5',
            'Odd'
        ), (
            'sample input: negative even',
            '-14',
            'Even'
        ), (
            'sample input: negative odd',
            '-27',
            'Odd'
        )
    ]
)


@pytest.fixture(params=sources[ProjectType.EvenOdd],
                ids=[source.name + source.extension for source in sources[ProjectType.EvenOdd]])
def even_odd(request):
    return request.param


@pytest.mark.parametrize(sorting_valid_permutations[0], sorting_valid_permutations[1],
                         ids=[p[0] for p in sorting_valid_permutations[1]])
def test_even_odd_valid(description, in_params, expected, docker_client, even_odd):
    actual = even_odd.run(docker_client, params=in_params)
    assert actual.replace('[', '').replace(']', '').strip() == expected


@pytest.mark.parametrize(sorting_invalid_permutations[0], sorting_invalid_permutations[1],
                         ids=[p[0] for p in sorting_invalid_permutations[1]])
def test_even_invalid(description, in_params, expected, docker_client, even_odd):
    actual = even_odd.run(docker_client, params=in_params, expect_error=True)
    assert actual.strip() == expected