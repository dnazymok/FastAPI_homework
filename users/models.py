from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str


class CreateUserParams(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: str
