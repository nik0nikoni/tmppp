class Course:
    def __init__(self, course_id: int, title: str, description: str, teacher_id: int):
        self.course_id = course_id
        self.title = title
        self.description = description
        self.teacher_id = teacher_id
        self.students = []

    def add_student(self, student_id: int) -> None:
        if student_id not in self.students:
            self.students.append(student_id)

    def get_course_type(self) -> str:
        raise NotImplementedError("Method get_course_type() must be implemented in subclasses")

    def get_info(self) -> str:
        return (
            f"Course(id={self.course_id}, title='{self.title}', "
            f"type='{self.get_course_type()}', teacher_id={self.teacher_id})"
        )


class VideoCourse(Course):
    def __init__(self, course_id: int, title: str, description: str, teacher_id: int, video_duration: int):
        super().__init__(course_id, title, description, teacher_id)
        self.video_duration = video_duration

    def get_course_type(self) -> str:
        return "video"


class TextCourse(Course):
    def __init__(self, course_id: int, title: str, description: str, teacher_id: int, pages_count: int):
        super().__init__(course_id, title, description, teacher_id)
        self.pages_count = pages_count

    def get_course_type(self) -> str:
        return "text"


class InteractiveCourse(Course):
    def __init__(self, course_id: int, title: str, description: str, teacher_id: int, tasks_count: int):
        super().__init__(course_id, title, description, teacher_id)
        self.tasks_count = tasks_count

    def get_course_type(self) -> str:
        return "interactive"