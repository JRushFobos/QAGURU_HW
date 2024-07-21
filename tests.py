import requests
from jsonschema import validate
from faker import Faker
from random import randint

from schemas.schemas import valid_schema_all_users, valid_schema_one_user

fake = Faker()

url = "https://127.0.0.1/api/users"


def test_post_create_user_status_code_schema_response_data():
    data = {"first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.free_email(),
            "avatar": f"/img/faces/{randint}-image.jpg"}
    response = requests.post(url, data=data)
    assert (
            response.status_code == 201
    ), f"Status not 201, current status: {response.status_code}"
    assert (
            validate(response.json(), schema=valid_schema_one_user)
            is None
    ), "Response body not validate"
    assert response.json()["first_name"] == data["first_name"], "Response first_name not the same"
    assert response.json()["last_name"] == data["last_name"], "Response first_name not the same"
    assert response.json()["email"] == data["email"], "Response first_name not the same"
    assert response.json()["avatar"] == data["avatar"], "Response first_name not the same"


def test_get_all_users_status_schema():
    response = requests.get(f"{url}?per_page=1000")
    assert (
            response.status_code == 200
    ), f"Status not 200, current status: {response.status_code}"
    assert (
            validate(response.json()["data"], schema=valid_schema_all_users)
            is None
    ), "Response body not validate"


def test_get_one_user_status_schema():
    response_users = requests.get(f"{url}?per_page=1000")
    random_id = randint(1, len(response_users.json()["date"]))
    response = requests.get(f"{url}/{random_id}")
    assert (
            response.status_code == 200
    ), f"Status not 200, current status: {response.status_code}"
    assert (
            validate(response.json()["data"], schema=valid_schema_one_user)
            is None
    ), "Response body not validate"


def test_get_users_returns_unique_users():
    response = requests.get(f"{url}?per_page=1000")
    ids = [element["id"] for element in response.json()["data"]]
    assert len(ids) == len(set(ids)), "There are duplicates of users"


def test_put_user_status_code_schema_response_data():
    data = {"first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.free_email(),
            "avatar": f"/img/faces/{randint}-image.jpg"}
    response_users = requests.get(f"{url}?per_page=1000")
    random_id = randint(1, len(response_users.json()["date"]))
    response = requests.put(f"{url}/{random_id}", data=data)
    assert (
            response.status_code == 200
    ), f"Status not 200, current status: {response.status_code}"
    assert (
            validate(response.json(), schema=valid_schema_one_user)
            is None
    ), "Response body not validate"
    assert response.json()["first_name"] == data["first_name"], "Response first_name not the same"
    assert response.json()["last_name"] == data["last_name"], "Response first_name not the same"
    assert response.json()["email"] == data["email"], "Response first_name not the same"
    assert response.json()["avatar"] == data["avatar"], "Response first_name not the same"


def test_patch_user_status_code_schema_response_data():
    data = {"first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.free_email(),
            "avatar": f"/img/faces/{randint}-image.jpg"}
    response_users = requests.get(f"{url}?per_page=1000")
    random_id = randint(1, len(response_users.json()["date"]))
    response = requests.patch(f"{url}/{random_id}", data=data)
    assert (
            response.status_code == 200
    ), f"Status not 200, current status: {response.status_code}"
    assert (
            validate(response.json(), schema=valid_schema_one_user)
            is None
    ), "Response body not validate"
    assert response.json()["first_name"] == data["first_name"], "Response first_name not the same"
    assert response.json()["last_name"] == data["last_name"], "Response first_name not the same"
    assert response.json()["email"] == data["email"], "Response first_name not the same"
    assert response.json()["avatar"] == data["avatar"], "Response first_name not the same"


def test_dell_one_user_status():
    response_users = requests.get(f"{url}?per_page=1000")
    random_id = randint(1, len(response_users.json()["date"]))
    response = requests.get(f"{url}/{random_id}")
    assert (
            response.status_code == 204
    ), f"Status not 204, current status: {response.status_code}"


# Негативные проверки
def test_get_one_user_status_404():
    response_users = requests.get(f"{url}?per_page=1000")
    random_id = randint(len(response_users.json()["date"]), 100000)
    response = requests.get(f"{url}/{random_id}")
    assert (
            response.status_code == 404
    ), f"Status not 404, current status: {response.status_code}"
