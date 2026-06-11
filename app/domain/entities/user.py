class User:
    def __init__(self, user_id: int, username: str, email: str, password: str, role: str):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def get_info(self) -> str:
        return (
            f"User(id={self.user_id}, username='{self.username}', "
            f"email='{self.email}', role='{self.role}')"
        )