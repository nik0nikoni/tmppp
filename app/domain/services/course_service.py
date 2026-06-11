from app.domain.patterns.factory_method import (
    VideoCourseFactory,
    TextCourseFactory,
    InteractiveCourseFactory
)
from app.repositories.course_repository import CourseRepository


class CourseService:
    def __init__(self, repository: CourseRepository | None = None):
        self.repository = repository or CourseRepository()

    def create_course(self, course_type: str, title: str, description: str, teacher_id: int, extra_value: int):
        factory = self._get_factory(course_type)

        course = factory.create_course(
            course_id=0,
            title=title,
            description=description,
            teacher_id=teacher_id,
            extra_value=extra_value
        )

        course.course_id = self.repository.create(course)
        return course

    def _get_factory(self, course_type: str):
        if course_type == "video":
            return VideoCourseFactory()
        elif course_type == "text":
            return TextCourseFactory()
        elif course_type == "interactive":
            return InteractiveCourseFactory()
        else:
            raise ValueError("Unknown course type")

    def get_all_courses(self):
        return self.repository.list_all()

    def get_course(self, course_id: int):
        return self.repository.get_by_id(course_id)
