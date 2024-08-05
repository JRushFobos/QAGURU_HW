import os
import dotenv

from faker import Faker
from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel, text

from app.models.models import User

dotenv.load_dotenv()
engine = create_engine(os.getenv("DATABASE_ENGINE"), pool_size=int(os.getenv("DATABASE_POOL_SIZE", 10)))

fake = Faker()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def check_and_fill_users():
    try:
        with Session(engine) as db:
            db.execute(text("SELECT 1"))
            if db.query(User).count() == 0:
                for _ in range(20):
                    db_user = User(
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        email=fake.unique.email(),
                        avatar=fake.image_url()
                    )
                    db.add(db_user)
                    db.commit()
        return True
    except Exception as e:
        print(e)
        return False
