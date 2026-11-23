import os

import pytest


@pytest.fixture
def practice_login_url() -> str:
    return os.getenv(
        "PRACTICE_LOGIN_URL",
        "https://practicetestautomation.com/practice-test-login/",
    )


@pytest.fixture
def practice_username() -> str:
    return os.getenv("PRACTICE_USERNAME", "student")


@pytest.fixture
def practice_password() -> str:
    return os.getenv("PRACTICE_PASSWORD", "Password123")
