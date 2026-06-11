from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserResponse
from app.domain.entities.user import User
from app.domain.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])

auth_service = AuthService()
user_repository = UserRepository()


@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate):
    try:
        user_id = user_repository.create(
            username=user_data.username,
            email=str(user_data.email),
            password=user_data.password,
            role=user_data.role,
        )
    except Exception as error:
        raise HTTPException(status_code=400, detail=str(error))

    return UserResponse(
        user_id=user_id,
        username=user_data.username,
        email=user_data.email,
        role=user_data.role
    )


@router.post("/login/{user_id}")
def login_user(user_id: int):
    row = user_repository.get_by_id(user_id)
    if row:
        user = User(
            user_id=row["id"],
            username=row["username"],
            email=row["email"],
            password="",
            role=row["role"],
        )
        auth_service.login(user)
        return {"message": f"User {user.username} logged in successfully"}

    raise HTTPException(status_code=404, detail="User not found")


@router.get("/active")
def get_active_users():
    active_users = auth_service.get_active_users()

    return [
        {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
        for user in active_users
    ]
