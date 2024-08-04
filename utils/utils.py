from faker import Faker
from sqlalchemy.orm import Session
from sqlmodel import text

from app.models.models import User
from app.database.engine import engine

fake = Faker()


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
