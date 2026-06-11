from app.database import get_connection


class CourseRepository:
    def create(self, course) -> int:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                INSERT INTO courses (title, description, teacher_id, course_type, extra_value)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    course.title,
                    course.description,
                    course.teacher_id,
                    course.get_course_type(),
                    self._get_extra_value(course),
                ),
            )
            return cursor.lastrowid

    def list_all(self) -> list[dict]:
        with get_connection() as connection:
            rows = connection.execute(
                "SELECT * FROM courses ORDER BY id DESC"
            ).fetchall()
            return [dict(row) for row in rows]

    def get_by_id(self, course_id: int) -> dict | None:
        with get_connection() as connection:
            row = connection.execute(
                "SELECT * FROM courses WHERE id = ?",
                (course_id,),
            ).fetchone()
            return dict(row) if row else None

    def _get_extra_value(self, course) -> int:
        return (
            getattr(course, "video_duration", None)
            or getattr(course, "pages_count", None)
            or getattr(course, "tasks_count", None)
            or 0
        )
