import pytest
from pathlib import Path


@pytest.fixture
def fix1(pytestconfig):
    # print("\nExecuting before init...\n")

    name = pytestconfig.getoption("name")
    # do something before each test function
    yield name
    p = Path("tests/data/merged.html")
    if p.is_file():
        p.unlink()
    # do something after each test function


def pytest_addoption(parser):
    parser.addoption("--name", action="store", default=None)
