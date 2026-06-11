from fastapi import Request

from app.repositories.user_repository import UserRepository


def get_current_user(request: Request) -> dict | None:
    user_id = request.cookies.get("user_id")
    if not user_id or not user_id.isdigit():
        return None
    return UserRepository().get_by_id(int(user_id))


def require_user_id(request: Request) -> int:
    user = get_current_user(request)
    if user is None:
        return 1
    return user["id"]
