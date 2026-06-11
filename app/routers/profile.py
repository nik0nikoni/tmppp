from fastapi import APIRouter, HTTPException

from app.domain.patterns.decorator import AvatarDecorator, BadgeDecorator, BasicProfile, ThemeDecorator
from app.repositories.user_repository import ProfileRepository

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/{user_id}")
def get_profile(user_id: int):
    profile = ProfileRepository().get(user_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    decorated = BasicProfile(profile["username"])

    if profile["avatar_url"]:
        decorated = AvatarDecorator(decorated, profile["avatar_url"])

    decorated = ThemeDecorator(decorated, profile["theme"])

    for badge in profile["badges"]:
        decorated = BadgeDecorator(decorated, badge)

    return decorated.get_data()
