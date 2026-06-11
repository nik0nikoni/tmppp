from dataclasses import dataclass


@dataclass
class CourseModel:
    id: int
    title: str
    description: str
    teacher_id: int
    course_type: str
    extra_value: int
