from __future__ import annotations

from abc import ABC, abstractmethod

from app.repositories.result_repository import ActivityLogRepository
from app.repositories.user_repository import ProfileRepository


class Command(ABC):
    name = "Command"

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class CommandBus:
    def __init__(self, activity_log_repository: ActivityLogRepository | None = None):
        self.activity_log_repository = activity_log_repository or ActivityLogRepository()

    def handle(self, command: Command):
        result = command.execute()
        self.activity_log_repository.create(
            getattr(command, "user_id", None),
            command.name,
            str(result),
        )
        return result


class ChangeThemeCommand(Command):
    name = "ChangeThemeCommand"

    def __init__(self, user_id: int, theme: str, profile_repository: ProfileRepository | None = None):
        self.user_id = user_id
        self.theme = theme
        self.profile_repository = profile_repository or ProfileRepository()

    def execute(self):
        profile = self.profile_repository.get(self.user_id)
        if profile is None:
            raise ValueError("User profile not found")

        self.profile_repository.update(
            user_id=self.user_id,
            avatar_url=profile["avatar_url"],
            theme=self.theme,
            badges=profile["badges"],
        )
        return {"theme": self.theme}


class UploadAvatarCommand(Command):
    name = "UploadAvatarCommand"

    def __init__(self, user_id: int, avatar_url: str, profile_repository: ProfileRepository | None = None):
        self.user_id = user_id
        self.avatar_url = avatar_url
        self.profile_repository = profile_repository or ProfileRepository()

    def execute(self):
        profile = self.profile_repository.get(self.user_id)
        if profile is None:
            raise ValueError("User profile not found")

        self.profile_repository.update(
            user_id=self.user_id,
            avatar_url=self.avatar_url,
            theme=profile["theme"],
            badges=profile["badges"],
        )
        return {"avatar_url": self.avatar_url}


class AddBadgeCommand(Command):
    name = "AddBadgeCommand"

    def __init__(self, user_id: int, badge: str, profile_repository: ProfileRepository | None = None):
        self.user_id = user_id
        self.badge = badge
        self.profile_repository = profile_repository or ProfileRepository()

    def execute(self):
        profile = self.profile_repository.get(self.user_id)
        if profile is None:
            raise ValueError("User profile not found")

        badges = list(profile["badges"])
        if self.badge not in badges:
            badges.append(self.badge)

        self.profile_repository.update(
            user_id=self.user_id,
            avatar_url=profile["avatar_url"],
            theme=profile["theme"],
            badges=badges,
        )
        return {"badge": self.badge}
