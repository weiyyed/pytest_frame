
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--custom", action="store", default="", help="my option: value"
    )

@pytest.fixture
def custom(request):
    return request.config.getoption("--custom")