from abc import ABC, abstractmethod


# 1. Общий интерфейс компонента
class UserProfile(ABC):
    @abstractmethod
    def get_info(self):
        pass


# 2. Базовый компонент
class BasicUserProfile(UserProfile):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    def get_info(self):
        return {
            "username": self.username,
            "email": self.email
        }


# 3. Базовый декоратор
class UserProfileDecorator(UserProfile):
    def __init__(self, profile: UserProfile):
        self.profile = profile

    def get_info(self):
        return self.profile.get_info()


# 4. Конкретный декоратор: добавляет аватар
class AvatarDecorator(UserProfileDecorator):
    def __init__(self, profile: UserProfile, avatar_url):
        super().__init__(profile)
        self.avatar_url = avatar_url

    def get_info(self):
        info = self.profile.get_info()
        info["avatar_url"] = self.avatar_url
        return info


# 5. Конкретный декоратор: добавляет статус
class StatusDecorator(UserProfileDecorator):
    def __init__(self, profile: UserProfile, status):
        super().__init__(profile)
        self.status = status

    def get_info(self):
        info = self.profile.get_info()
        info["status"] = self.status
        return info


# 6. Конкретный декоратор: добавляет роль
class RoleDecorator(UserProfileDecorator):
    def __init__(self, profile: UserProfile, role):
        super().__init__(profile)
        self.role = role

    def get_info(self):
        info = self.profile.get_info()
        info["role"] = self.role
        return info


# Пример использования
profile = BasicUserProfile(
    username="andrei",
    email="andrei@example.com"
)

profile = AvatarDecorator(profile, "avatar.png")
profile = StatusDecorator(profile, "Online")
profile = RoleDecorator(profile, "Student")

print(profile.get_info())