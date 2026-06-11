from app.repositories.course_repository import CourseRepository
from app.repositories.result_repository import ActivityLogRepository, NotificationRepository
from app.repositories.user_repository import UserRepository
from app.database import get_connection


class LearningFacade:
    def __init__(
        self,
        user_repository: UserRepository | None = None,
        course_repository: CourseRepository | None = None,
        notification_repository: NotificationRepository | None = None,
        activity_log_repository: ActivityLogRepository | None = None,
    ):
        self.user_repository = user_repository or UserRepository()
        self.course_repository = course_repository or CourseRepository()
        self.notification_repository = notification_repository or NotificationRepository()
        self.activity_log_repository = activity_log_repository or ActivityLogRepository()

    def enroll_user_to_course(self, user_id: int, course_id: int) -> dict:
        user = self.user_repository.get_by_id(user_id)
        if user is None:
            raise ValueError("User not found")

        course = self.course_repository.get_by_id(course_id)
        if course is None:
            raise ValueError("Course not found")

        with get_connection() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO enrollments (user_id, course_id, progress)
                VALUES (?, ?, 0)
                """,
                (user_id, course_id),
            )

        message = f"{user['username']} enrolled in {course['title']}"
        self.notification_repository.create(user_id, "system", message)
        self.activity_log_repository.create(user_id, "EnrollCourseFacade", message)

        return {
            "user_id": user_id,
            "course_id": course_id,
            "message": message,
        }

    def dashboard(self, user_id: int) -> dict:
        with get_connection() as connection:
            enrollments = connection.execute(
                """
                SELECT e.*, c.title, c.course_type
                FROM enrollments e
                JOIN courses c ON c.id = e.course_id
                WHERE e.user_id = ?
                ORDER BY e.id DESC
                """,
                (user_id,),
            ).fetchall()
            notifications = connection.execute(
                """
                SELECT *
                FROM notifications
                WHERE user_id = ? OR user_id IS NULL
                ORDER BY id DESC
                LIMIT 5
                """,
                (user_id,),
            ).fetchall()

        return {
            "enrollments": [dict(row) for row in enrollments],
            "notifications": [dict(row) for row in notifications],
        }
