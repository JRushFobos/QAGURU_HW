from http import HTTPStatus
from fastapi import APIRouter

from app.database.engine import check_and_fill_users
from app.models.AppStatus import AppStatus


router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(database=check_and_fill_users())

