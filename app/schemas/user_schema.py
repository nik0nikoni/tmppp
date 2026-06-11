from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    password: str
    role: str


class UserResponse(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    role: str