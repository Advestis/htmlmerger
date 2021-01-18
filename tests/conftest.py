import pytest

@pytest.fixture
def fix1(pytestconfig):
    # print("\nExecuting before init...\n")

    name = pytestconfig.getoption("name")
    # do something before each test function
    yield name
    # do something after each test function


def pytest_addoption(parser):
    parser.addoption("--name", action="store", default=None)
