import pytest
import requests
from random import randint

from faker import Faker

from app.models.models import PaginatedResponse

fake = Faker()


# Tecты пагинации
def test_attrs_pagination(app_url):
    response = requests.get(f"{app_url}/api/users")
    PaginatedResponse(**response.json())


# ожидаемое количество объектов в ответе;
def test_objs_in_resp_pagination(app_url):
    response = requests.get(f"{app_url}/api/users")
    count = len(response.json()["items"])
    random_size = randint(1,count)
    response = requests.get(f"{app_url}/api/users/?size={random_size}")
    assert random_size == len(response.json()["items"]), f"Count obj not the same"


# правильное количество страниц при разных значениях size;
@pytest.mark.parametrize("size", [1, 5, 10, 25])
def test_count_pages_by_size_pagination(app_url, size, check_empty_database):
    response = requests.get(f"{app_url}/api/users")
    count_users = response.json()["total"]
    response = requests.get(f"{app_url}/api/users/?size={size}")
    expected_pages = (count_users + size - 1) // size
    assert response.json()["pages"] == expected_pages, \
        f"{expected_pages} pages were expected, but {response.json()['pages']} as received"
    items_count = len(response.json()["items"])
    assert items_count <= size, "The number of elements on the page must not exceed the page size"


# возвращаются разные данные при разных значениях size;
def test_resp_by_size_pagination(app_url):
    response = requests.get(f"{app_url}/api/users")
    count = len(response.json()["items"])
    random_size = randint(2,count)
    response = requests.get(f"{app_url}/api/users/?size={random_size}")
    response_size_1 = response.json()["items"]
    response = requests.get(f"{app_url}/api/users/?size={random_size-1}")
    response_size_2 = response.json()["items"]
    assert (response_size_1 != response_size_2), "Response the same"


# возвращаются разные данные при разных значениях page;
@pytest.mark.parametrize("page", [2, 5, 10, 15])
def test_diff_resp_by_page(app_url, page):
    response = requests.get(f"{app_url}/api/users/?size=1&page={page}")
    response_page_1 = response.json()["items"]
    response = requests.get(f"{app_url}/api/users/?size=1&page={page+1}")
    response_page_2 = response.json()["items"]
    assert (response_page_1 != response_page_2), "Response the same"
