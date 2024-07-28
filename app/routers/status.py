from http import HTTPStatus
from fastapi import APIRouter

from app.database.engine import check_availability
from app.models.AppStatus import AppStatus
from utils.utils import check_and_fill_users

router = APIRouter()


@router.get("/status", status_code=HTTPStatus.OK)
def status() -> AppStatus:
    return AppStatus(database=check_availability())


@router.on_event("startup")
def startup_event():
    check_and_fill_users()
