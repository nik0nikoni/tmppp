class Profile:
    def get_data(self) -> dict:
        raise NotImplementedError("Method get_data() must be implemented")


class BasicProfile(Profile):
    def __init__(self, username: str):
        self.username = username

    def get_data(self) -> dict:
        return {
            "username": self.username,
            "avatar": None,
            "theme": "light",
            "badges": []
        }


class ProfileDecorator(Profile):
    def __init__(self, profile: Profile):
        self._profile = profile

    def get_data(self) -> dict:
        return self._profile.get_data()


class AvatarDecorator(ProfileDecorator):
    def __init__(self, profile: Profile, avatar_url: str):
        super().__init__(profile)
        self.avatar_url = avatar_url

    def get_data(self) -> dict:
        data = self._profile.get_data()
        data["avatar"] = self.avatar_url
        return data


class ThemeDecorator(ProfileDecorator):
    def __init__(self, profile: Profile, theme: str):
        super().__init__(profile)
        self.theme = theme

    def get_data(self) -> dict:
        data = self._profile.get_data()
        data["theme"] = self.theme
        return data


class BadgeDecorator(ProfileDecorator):
    def __init__(self, profile: Profile, badge: str):
        super().__init__(profile)
        self.badge = badge

    def get_data(self) -> dict:
        data = self._profile.get_data()
        badges = list(data["badges"])
        badges.append(self.badge)
        data["badges"] = badges
        return data