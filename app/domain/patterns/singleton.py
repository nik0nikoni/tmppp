class UserManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserManager, cls).__new__(cls)
            cls._instance._active_users = []
        return cls._instance

    def login(self, user):
        if user not in self._active_users:
            self._active_users.append(user)

    def logout(self, user):
        if user in self._active_users:
            self._active_users.remove(user)

    def get_active_users(self):
        return self._active_users

    def is_logged_in(self, user) -> bool:
        return user in self._active_users

    def check_role(self, user, role: str) -> bool:
        return user.role == role