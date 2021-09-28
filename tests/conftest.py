import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--api_key", action="store", default="", help="Valid API key."
    )


@pytest.fixture
def api_key(request):
    return request.config.getoption("--api_key")
