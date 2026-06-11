from fastapi import APIRouter, HTTPException
from app.schemas.course_schema import CourseCreate, CourseResponse
from app.domain.services.course_service import CourseService

router = APIRouter(prefix="/courses", tags=["Courses"])

course_service = CourseService()


@router.post("/create", response_model=CourseResponse)
def create_course(course_data: CourseCreate):
    try:
        course = course_service.create_course(
            course_type=course_data.course_type,
            title=course_data.title,
            description=course_data.description,
            teacher_id=course_data.teacher_id,
            extra_value=course_data.extra_value
        )

        return CourseResponse(
            course_id=course.course_id,
            title=course.title,
            description=course.description,
            teacher_id=course.teacher_id,
            course_type=course.get_course_type()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[CourseResponse])
def get_courses():
    courses = course_service.get_all_courses()

    return [
        CourseResponse(
            course_id=course["id"],
            title=course["title"],
            description=course["description"],
            teacher_id=course["teacher_id"],
            course_type=course["course_type"]
        )
        for course in courses
    ]
