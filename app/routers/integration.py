from fastapi import APIRouter
from app.domain.patterns.adapter import (
    MoodleSystem,
    GoogleClassroomSystem,
    MoodleAdapter,
    GoogleClassroomAdapter
)

router = APIRouter(prefix="/integration", tags=["Integration"])


@router.post("/enroll")
def enroll_student(system: str, student_name: str, course_name: str):
    if system == "moodle":
        adapter = MoodleAdapter(MoodleSystem())
    elif system == "google":
        adapter = GoogleClassroomAdapter(GoogleClassroomSystem())
    else:
        return {"error": "Unknown system"}

    result = adapter.enroll(student_name, course_name)

    return {
        "system": system,
        "result": result
    }