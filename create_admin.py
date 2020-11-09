from app.database import SessionLocal
from app.users import schemas, crud


db = SessionLocal()
data = {
    "username": "admin",
    "password": "admin1234"
}
crud.create_admin_user(db, schemas.UserCreate(**data))