import json

from app.database import get_connection


class ResultRepository:
    def create(self, user_id: int, test_id: int, result: dict, answers: dict) -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO test_results (user_id, test_id, score, max_score, passed, answers)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    test_id,
                    result["score"],
                    result["max_score"],
                    1 if result["passed"] else 0,
                    json.dumps(answers),
                ),
            )
            return cursor.lastrowid

    def list_recent(self, limit: int = 10) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT r.*, u.username, t.title AS test_title
                FROM test_results r
                JOIN users u ON u.id = r.user_id
                JOIN tests t ON t.id = r.test_id
                ORDER BY r.id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]


class NotificationRepository:
    def create(self, user_id: int | None, channel: str, message: str) -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO notifications (user_id, channel, message) VALUES (?, ?, ?)",
                (user_id, channel, message),
            )
            return cursor.lastrowid

    def list_recent(self, limit: int = 10) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM notifications ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]


class ActivityLogRepository:
    def create(self, user_id: int | None, command_name: str, details: str) -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                "INSERT INTO activity_logs (user_id, command_name, details) VALUES (?, ?, ?)",
                (user_id, command_name, details),
            )
            return cursor.lastrowid

    def list_recent(self, limit: int = 20) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT a.*, u.username
                FROM activity_logs a
                LEFT JOIN users u ON u.id = a.user_id
                ORDER BY a.id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]
