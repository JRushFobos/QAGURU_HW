from http import HTTPStatus
from fastapi import HTTPException, APIRouter, Depends
from fastapi_pagination import Page, paginate, Params

from app.database import users
from app.models.models import UserCreate, User, UserUpdate

router = APIRouter(prefix="/api/users")


@router.post("/",  status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    UserCreate.model_validate(user.model_dump())
    return users.create_user(user)


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def read_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.delete("/{user_id}", status_code=HTTPStatus.NO_CONTENT)
def delete_user(user_id: int):
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    users.delete_user(user_id)
    return {"message": "User deleted"}


@router.get("/", response_model=Page[User], status_code=HTTPStatus.OK)
def get_users(params: Params = Depends()) -> Page[User]:
    user_list = users.get_users()
    return paginate(user_list, params)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.put("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: UserUpdate) -> User:
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)

