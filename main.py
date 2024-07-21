import sqlite3
from fastapi import FastAPI, HTTPException
from typing import List

from models.models import UserData


app = FastAPI()


# Создание базы данных и таблицы
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT,
            first_name TEXT,
            last_name TEXT,
            avatar TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Инициализация базы данных
init_db()


# Метод POST для добавления пользователя
@app.post("/api/users/", response_model=UserData)
def create_user(user: UserData):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (email, first_name, last_name, avatar) VALUES (?, ?, ?, ?)
    ''', (user.email, user.first_name, user.last_name, user.avatar))
    conn.commit()
    user.id = cursor.lastrowid  # Получаем ID последней вставленной записи
    conn.close()
    return user


# Метод GET для получения всех пользователей
@app.get("/api/users/", response_model=List[UserData])
def get_users():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()

    return [UserData(id=row[0], email=row[1], first_name=row[2], last_name=row[3], avatar=row[4]) for row in users]


# Метод GET для получения пользователя по ID
@app.get("/api/users/{user_id}", response_model=UserData)
def get_user(user_id: int):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return UserData(id=user[0], email=user[1], first_name=user[2], last_name=user[3], avatar=user[4])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
