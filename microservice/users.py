import dotenv
from fastapi import FastAPI, HTTPException, status
from typing import List
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.ext.sqlalchemy import paginate

from models.AppStatus import AppStatus
from models.models import UserResponse, UserCreate, engine, User, UserUpdate, PaginatedResponse
from utils.utils import check_and_fill_users

app = FastAPI()
add_pagination(app)
dotenv.load_dotenv()


@app.on_event("startup")
def startup_event():
    check_and_fill_users()


@app.get("/status", status_code=status.HTTP_200_OK)
def status_app() -> AppStatus:
    return AppStatus(users=True)


@app.post("/api/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    with Session(engine) as db:
        db_user = User(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            avatar=str(user.avatar)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int):
    with Session(engine) as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user


@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    with Session(engine) as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        db.delete(user)
        db.commit()
        return {"message": "User deleted successfully"}


@app.get("/api/users/", response_model=PaginatedResponse)
def read_users(skip: int = 0, size: int = 10) -> PaginatedResponse:
    with Session(engine) as db:
        total = db.query(User).count()
        users = db.query(User).offset(skip).limit(size).all()

        page = skip // size + 1
        pages = (total + size - 1) // size

        user_items = [UserResponse(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            avatar=str(user.avatar)
        ) for user in users]

        return PaginatedResponse(
            total=total,
            page=page,
            size=size,
            pages=pages,
            items=user_items
        )


@app.patch("/api/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    with Session(engine) as db:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        for attr, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, attr, value)

        db.commit()
        db.refresh(db_user)
        return db_user


@app.put("/api/users/{user_id}", response_model=UserResponse)
def update_user_put(user_id: int, user_update: UserCreate):
    with Session(engine) as db:
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        db_user.email = user_update.email
        db_user.first_name = user_update.first_name
        db_user.last_name = user_update.last_name
        db_user.avatar = str(user_update.avatar)

        db.commit()
        db.refresh(db_user)
        return db_user


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
