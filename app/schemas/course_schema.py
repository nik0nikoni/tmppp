from pydantic import BaseModel


class CourseCreate(BaseModel):
    course_type: str
    title: str
    description: str
    teacher_id: int
    extra_value: int


class CourseResponse(BaseModel):
    course_id: int
    title: str
    description: str
    teacher_id: int
    course_type: str