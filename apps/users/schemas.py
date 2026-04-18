from ninja import Schema
from .models import User
from datetime import date

class UserRead(Schema):
    user_id: int|None
    username: str
    email: str
    name: str
    phone_number: str

class UserCreate(Schema):
    username: str
    email: str
    name: str
    password: str
    cpf: str
    phone_number: str
    date_of_birth: date

class UserUpdate(Schema):
    username: str | None = None
    email: str | None
    name: str | None = None
    password: str | None = None
    cpf: str | None = None
    phone_number: str | None = None
    date_of_birth: date | None = None