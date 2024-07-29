from fastapi import status

import pytest
import requests


@pytest.mark.order(1)
def test_app_status_code(app_url):
    response = requests.get(f"{app_url}/status")
    assert (response.status_code == status.HTTP_200_OK), f"Status not 200, current status: {response.status_code}"