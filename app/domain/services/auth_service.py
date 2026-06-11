from app.domain.patterns.singleton import UserManager


class AuthService:
    def __init__(self):
        self.user_manager = UserManager()

    def login(self, user):
        self.user_manager.login(user)

    def logout(self, user):
        self.user_manager.logout(user)

    def get_active_users(self):
        return self.user_manager.get_active_users()