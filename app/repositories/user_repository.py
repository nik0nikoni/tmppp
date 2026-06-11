from app.database import get_connection


class UserRepository:
    def create(self, username: str, email: str, password: str, role: str) -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (username, email, password, role)
                VALUES (?, ?, ?, ?)
                """,
                (username, email, password, role),
            )
            user_id = cursor.lastrowid
            connection.execute(
                "INSERT INTO user_profiles (user_id) VALUES (?)",
                (user_id,),
            )
            return user_id

    def list_all(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT id, username, email, role, created_at FROM users ORDER BY id DESC"
            ).fetchall()
            return [dict(row) for row in rows]

    def get_by_id(self, user_id: int) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT id, username, email, password, role, created_at FROM users WHERE id = ?",
                (user_id,),
            ).fetchone()
            return dict(row) if row else None

    def get_by_email(self, email: str) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT id, username, email, password, role, created_at FROM users WHERE email = ?",
                (email,),
            ).fetchone()
            return dict(row) if row else None


class ProfileRepository:
    def get(self, user_id: int) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                """
                SELECT u.id AS user_id, u.username, p.avatar_url, p.theme, p.badges
                FROM users u
                JOIN user_profiles p ON p.user_id = u.id
                WHERE u.id = ?
                """,
                (user_id,),
            ).fetchone()
            if not row:
                return None
            data = dict(row)
            data["badges"] = [badge for badge in data["badges"].split(",") if badge]
            data["avatar"] = data["avatar_url"]
            return data

    def update(self, user_id: int, avatar_url: str | None, theme: str, badges: list[str]):
        with get_connection() as connection:
            connection.execute(
                """
                UPDATE user_profiles
                SET avatar_url = ?, theme = ?, badges = ?
                WHERE user_id = ?
                """,
                (avatar_url, theme, ",".join(badges), user_id),
            )
