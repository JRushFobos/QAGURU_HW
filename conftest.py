import os

import dotenv
import pytest
import requests


@pytest.fixture(scope="session", autouse=True)
def envs():
    dotenv.load_dotenv()


@pytest.fixture(scope="session")
def app_url():
    return os.getenv("APP_URL")


@pytest.fixture(scope="session")
def check_empty_database(app_url):
    response = requests.get(f"{app_url}/api/users")
    count_users = response.json()["total"]
    if count_users == 0:
        pytest.skip(f"Database is not empty, {count_users} users found.")
