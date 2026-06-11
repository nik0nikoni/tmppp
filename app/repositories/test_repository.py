import json

from app.database import get_connection


class QuestionRepository:
    def create(self, question) -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO questions (id, question_type, text, difficulty, options, correct_answer, points)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    question.question_id if question.question_id else None,
                    question.__class__.__name__,
                    question.text,
                    question.difficulty,
                    json.dumps(getattr(question, "options", None)),
                    str(question.correct_answer),
                    question.points,
                ),
            )
            return cursor.lastrowid

    def list_all(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute("SELECT * FROM questions ORDER BY id DESC").fetchall()
            return [self._decode(dict(row)) for row in rows]

    def get_by_id(self, question_id: int) -> dict | None:
        with get_connection() as connection:
            row = connection.execute("SELECT * FROM questions WHERE id = ?", (question_id,)).fetchone()
            return self._decode(dict(row)) if row else None

    def _decode(self, row: dict) -> dict:
        row["options"] = json.loads(row["options"]) if row["options"] else None
        return row


class TestRepository:
    def create(self, test) -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tests (course_id, title, time_limit, pass_score, max_attempts)
                VALUES (?, ?, ?, ?, ?)
                """,
                (test.course_id, test.title, test.time_limit, test.pass_score, test.max_attempts),
            )
            test_id = cursor.lastrowid
            for question in test.questions:
                connection.execute(
                    "INSERT INTO test_questions (test_id, question_id) VALUES (?, ?)",
                    (test_id, question.question_id),
                )
            return test_id

    def list_all(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                """
                SELECT t.*, COUNT(tq.question_id) AS questions_count
                FROM tests t
                LEFT JOIN test_questions tq ON tq.test_id = t.id
                GROUP BY t.id
                ORDER BY t.id DESC
                """
            ).fetchall()
            return [dict(row) for row in rows]

    def get_with_questions(self, test_id: int) -> tuple[dict, list[dict]] | None:
        with get_connection() as connection:
            test = connection.execute("SELECT * FROM tests WHERE id = ?", (test_id,)).fetchone()
            if not test:
                return None
            questions = connection.execute(
                """
                SELECT q.*
                FROM questions q
                JOIN test_questions tq ON tq.question_id = q.id
                WHERE tq.test_id = ?
                ORDER BY q.id
                """,
                (test_id,),
            ).fetchall()
            decoded = []
            for row in questions:
                item = dict(row)
                item["options"] = json.loads(item["options"]) if item["options"] else None
                decoded.append(item)
            return dict(test), decoded
