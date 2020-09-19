import pytest


@pytest.fixture()
def test_dir(request):
    return request.config.getoption("test_dir")


@pytest.fixture()
def source_dir(request):
    return request.config.getoption("source_dir")