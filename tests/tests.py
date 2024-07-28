import json
import requests
from random import randint

from jsonschema import validate
from faker import Faker

from schemas.schemas import valid_schema_all_users, valid_schema_one_user

fake = Faker()


def test_post_create_user_status_code_schema_response_data(app_url):
    data = {"first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.free_email(),
            "avatar": f"https://reqres.in/img/faces/{randint(1,1000)}-image.jpg"}
    response = requests.post(url=f"{app_url}/api/users", data=json.dumps(data))
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


def test_get_all_users_status_schema(app_url):
    response = requests.get(f"{app_url}/api/users")
    assert (
            response.status_code == 200
    ), f"Status not 200, current status: {response.status_code}"
    assert (
            validate(response.json()["items"], schema=valid_schema_all_users)
            is None
    ), "Response body not validate"


def test_get_one_user_status_schema(app_url):
    response_users = requests.get(f"{app_url}/api/users")
    random_id = randint(1, len(response_users.json()))
    response = requests.get(f"{app_url}/api/users/{random_id}")
    assert (
            response.status_code == 200
    ), f"Status not 200, current status: {response.status_code}"
    assert (
            validate(response.json(), schema=valid_schema_one_user)
            is None
    ), "Response body not validate"


def test_get_users_returns_unique_users(app_url):
    response = requests.get(f"{app_url}/api/users")
    ids = [element["id"] for element in response.json()["items"]]
    assert len(ids) == len(set(ids)), "There are duplicates of users"


def test_put_user_status_code_schema_response_data(app_url):
    data = {"first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.free_email(),
            "avatar": f"https://reqres.in/img/faces/{randint(1,1000)}-image.jpg"}
    response = requests.post(url=f"{app_url}/api/users", data=json.dumps(data))
    userid = response.json()["id"]
    data_update = {"first_name": fake.first_name(),
                   "last_name": fake.last_name(),
                   "email": fake.free_email(),
                   "avatar": f"https://reqres.in/img/faces/{randint(1,1000)}-image.jpg"}
    response = requests.put(url=f"{app_url}/api/users/{userid}", data=json.dumps(data_update))
    assert (
            response.status_code == 200
    ), f"Status not 200, current status: {response.status_code}"
    assert (
            validate(response.json(), schema=valid_schema_one_user)
            is None
    ), "Response body not validate"
    assert response.json()["first_name"] == data_update["first_name"], "Response first_name not the same"
    assert response.json()["last_name"] == data_update["last_name"], "Response first_name not the same"
    assert response.json()["email"] == data_update["email"], "Response first_name not the same"
    assert response.json()["avatar"] == data_update["avatar"], "Response first_name not the same"


def test_patch_user_status_code_schema_response_data(app_url):
    data = {"first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.free_email(),
            "avatar": f"https://reqres.in/img/faces/{randint(1,1000)}-image.jpg"}
    response = requests.post(url=f"{app_url}/api/users/", data=json.dumps(data))
    userid = response.json()["id"]
    data_update = {"first_name": fake.first_name(),
                   "last_name": fake.last_name(),
                   "email": fake.free_email(),
                   "avatar": f"https://reqres.in/img/faces/{randint(1,1000)}-image.jpg"}
    response = requests.patch(url=f"{app_url}/api/users/{userid}", data=json.dumps(data_update))
    assert (
            response.status_code == 200
    ), f"Status not 200, current status: {response.status_code}"
    assert (
            validate(response.json(), schema=valid_schema_one_user)
            is None
    ), "Response body not validate"
    assert response.json()["first_name"] == data_update["first_name"], "Response first_name not the same"
    assert response.json()["last_name"] == data_update["last_name"], "Response first_name not the same"
    assert response.json()["email"] == data_update["email"], "Response first_name not the same"
    assert response.json()["avatar"] == data_update["avatar"], "Response first_name not the same"


def test_dell_one_user_status(app_url):
    data = {"first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.free_email(),
            "avatar": f"https://reqres.in/img/faces/{randint(1,1000)}-image.jpg"}
    response = requests.post(url=f"{app_url}/api/users/", data=json.dumps(data))
    userid = response.json()["id"]
    response = requests.delete(f"{app_url}/api/users/{userid}")
    assert (
            response.status_code == 204
    ), f"Status not 204, current status: {response.status_code}"


# Tecты пагинации
def test_attrs_pagination(app_url):
    response = requests.get(f"{app_url}/api/users")
    pagination_attrs = ["total", "page", "size", "pages"]
    for attr in pagination_attrs:
        assert attr in response.json(), f"Attribute {attr} is missing "


# ожидаемое количество объектов в ответе;
def test_objs_in_resp_pagination(app_url):
    response = requests.get(f"{app_url}/api/users")
    count = len(response.json()["items"])
    random_size = randint(1,count)
    response = requests.get(f"{app_url}/api/users/?size={random_size}")
    assert random_size == len(response.json()["items"]), f"Count obj not the same"


# правильное количество страниц при разных значениях size;
def test_count_pages_by_size_pagination(app_url):
    response = requests.get(f"{app_url}/api/users")
    pagination_data = response.json()
    count_users = pagination_data["total"]
    assert count_users > 0, "BD is empty"

    for size in [1, 5, 10, 25, count_users]:
        response = requests.get(f"{app_url}/api/users/?size={size}")
        assert response.status_code == 200, "Error with pagination"

        pagination_data = response.json()
        expected_pages = (count_users + size - 1) // size

        # Проверяем, что количество страниц соответствует ожиданиям
        assert pagination_data["pages"] == expected_pages, \
            f"{expected_pages} pages were expected, but {pagination_data['pages']} as received"

        # Дополнительная проверка: количество элементов на странице не должно превышать size
        items_count = len(pagination_data["items"])
        assert items_count <= size, "The number of elements on the page must not exceed the page size"


# возвращаются разные данные при разных значениях page;
def test_resp_by_size_pagination(app_url):
    response = requests.get(f"{app_url}/api/users")
    count = len(response.json()["items"])
    random_size = randint(2,count)
    response = requests.get(f"{app_url}/api/users/?size={random_size}")
    response_size_1 = response.json()["items"]
    response = requests.get(f"{app_url}/api/users/?size={random_size-1}")
    response_size_2 = response.json()["items"]
    assert (response_size_1 != response_size_2), "Response the same"


# Негативные проверки
def test_get_one_user_status_404(app_url):
    response_users = requests.get(url=f"{app_url}/api/users/")
    random_id = randint(len(response_users.json()["items"]), 100000)
    response = requests.get(f"{app_url}/api/users/{random_id}")
    assert (
            response.status_code == 404
    ), f"Status not 404, current status: {response.status_code}"
