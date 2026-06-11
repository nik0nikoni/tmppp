from app.domain.entities.course import VideoCourse, TextCourse, InteractiveCourse


class CourseFactory:
    def create_course(self, course_id: int, title: str, description: str, teacher_id: int, extra_value: int):
        raise NotImplementedError("Method create_course() must be implemented in subclasses")


class VideoCourseFactory(CourseFactory):
    def create_course(self, course_id: int, title: str, description: str, teacher_id: int, extra_value: int):
        return VideoCourse(
            course_id=course_id,
            title=title,
            description=description,
            teacher_id=teacher_id,
            video_duration=extra_value
        )


class TextCourseFactory(CourseFactory):
    def create_course(self, course_id: int, title: str, description: str, teacher_id: int, extra_value: int):
        return TextCourse(
            course_id=course_id,
            title=title,
            description=description,
            teacher_id=teacher_id,
            pages_count=extra_value
        )


class InteractiveCourseFactory(CourseFactory):
    def create_course(self, course_id: int, title: str, description: str, teacher_id: int, extra_value: int):
        return InteractiveCourse(
            course_id=course_id,
            title=title,
            description=description,
            teacher_id=teacher_id,
            tasks_count=extra_value
        )