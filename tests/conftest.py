import pytest
from src.api_client import ApiClient


@pytest.fixture(scope="session")
def api():
    """One shared client per run: fixtures remove duplicated setup."""
    return ApiClient()
