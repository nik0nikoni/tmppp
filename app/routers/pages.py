import shutil
from pathlib import Path

from fastapi import APIRouter, Request, Form, UploadFile, File
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.routers.courses import course_service
from app.routers.tests import (
    question_from_row,
    question_repository,
    test_repository,
    test_service,
)
from app.database import UPLOAD_DIR
from app.auth import get_current_user, require_user_id
from app.domain.patterns.command import (
    AddBadgeCommand,
    ChangeThemeCommand,
    CommandBus,
    UploadAvatarCommand,
)
from app.domain.patterns.facade import LearningFacade
from app.repositories.user_repository import ProfileRepository, UserRepository

from app.domain.patterns.decorator import (
    BasicProfile,
    AvatarDecorator,
    ThemeDecorator,
    BadgeDecorator
)

from app.domain.patterns.adapter import (
    MoodleSystem,
    GoogleClassroomSystem,
    MoodleAdapter,
    GoogleClassroomAdapter
)

router = APIRouter(tags=["Pages"])

templates = Jinja2Templates(directory="app/templates")
command_bus = CommandBus()
learning_facade = LearningFacade()


@router.get("/")
def home_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"current_user": get_current_user(request)}
    )


@router.get("/pages/auth")
def auth_page(request: Request, success: str = "", error: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="auth.html",
        context={
            "current_user": get_current_user(request),
            "success_message": success,
            "error_message": error,
        },
    )


@router.post("/pages/auth/register")
def register_from_page(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    role: str = Form("student"),
):
    try:
        user_id = UserRepository().create(username, email, password, role)
        response = RedirectResponse(url="/pages/profile", status_code=303)
        response.set_cookie("user_id", str(user_id), httponly=True, samesite="lax")
        return response
    except Exception as error:
        return RedirectResponse(url=f"/pages/auth?error={str(error)}", status_code=303)


@router.post("/pages/auth/login")
def login_from_page(email: str = Form(...), password: str = Form(...)):
    user = UserRepository().get_by_email(email)
    if user is None or user["password"] != password:
        return RedirectResponse(url="/pages/auth?error=Invalid email or password", status_code=303)

    response = RedirectResponse(url="/pages/dashboard", status_code=303)
    response.set_cookie("user_id", str(user["id"]), httponly=True, samesite="lax")
    return response


@router.post("/pages/auth/logout")
def logout_from_page():
    response = RedirectResponse(url="/pages/auth?success=Logged out", status_code=303)
    response.delete_cookie("user_id")
    return response


@router.get("/pages/courses")
def courses_page(request: Request, success: str = "", error: str = ""):
    courses = course_service.get_all_courses()

    course_data = [
        {
            "course_id": course["id"],
            "title": course["title"],
            "description": course["description"],
            "teacher_id": course["teacher_id"],
            "course_type": course["course_type"],
            "extra_value": course["extra_value"],
        }
        for course in courses
    ]

    return templates.TemplateResponse(
        request=request,
        name="courses.html",
        context={
            "courses": course_data,
            "success_message": success,
            "error_message": error,
            "current_user": get_current_user(request),
        }
    )


@router.post("/pages/courses/create")
def create_course_from_page(
    course_type: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    teacher_id: int = Form(...),
    extra_value: int = Form(...)
):
    try:
        course_service.create_course(
            course_type=course_type,
            title=title,
            description=description,
            teacher_id=teacher_id,
            extra_value=extra_value
        )
        return RedirectResponse(
            url="/pages/courses?success=Course created successfully",
            status_code=303
        )
    except ValueError as e:
        return RedirectResponse(
            url=f"/pages/courses?error={str(e)}",
            status_code=303
        )


@router.get("/pages/tests")
def tests_page(request: Request, success: str = "", error: str = ""):
    question_data = [
        {
            "question_id": question["id"],
            "text": question["text"],
            "difficulty": question["difficulty"],
            "points": question["points"],
            "type": question["question_type"]
        }
        for question in question_repository.list_all()
    ]

    test_data = [
        {
            "test_id": test["id"],
            "title": test["title"],
            "course_id": test["course_id"],
            "questions_count": test["questions_count"],
            "time_limit": test["time_limit"],
            "pass_score": test["pass_score"],
            "max_attempts": test["max_attempts"]
        }
        for test in test_repository.list_all()
    ]

    return templates.TemplateResponse(
        request=request,
        name="tests.html",
        context={
            "questions": question_data,
            "tests": test_data,
            "success_message": success,
            "error_message": error,
            "current_user": get_current_user(request),
        }
    )


@router.post("/pages/tests/questions/multiple-choice/create")
def create_multiple_choice_question_from_page(
    question_id: int = Form(...),
    text: str = Form(...),
    difficulty: str = Form(...),
    options: str = Form(...),
    correct_answer: str = Form(...),
    points: int = Form(...)
):
    try:
        parsed_options = [option.strip() for option in options.split(",") if option.strip()]

        if not parsed_options:
            return RedirectResponse(
                url="/pages/tests?error=Options cannot be empty",
                status_code=303
            )

        question = test_service.create_multiple_choice_question(
            question_id=question_id,
            text=text,
            difficulty=difficulty,
            options=parsed_options,
            correct_answer=correct_answer,
            points=points
        )
        question_repository.create(question)

        return RedirectResponse(
            url="/pages/tests?success=Multiple choice question created successfully",
            status_code=303
        )
    except Exception:
        return RedirectResponse(
            url="/pages/tests?error=Failed to create multiple choice question",
            status_code=303
        )


@router.post("/pages/tests/questions/open/create")
def create_open_question_from_page(
    question_id: int = Form(...),
    text: str = Form(...),
    difficulty: str = Form(...),
    correct_answer: str = Form(...),
    points: int = Form(...)
):
    try:
        question = test_service.create_open_question(
            question_id=question_id,
            text=text,
            difficulty=difficulty,
            correct_answer=correct_answer,
            points=points
        )
        question_repository.create(question)

        return RedirectResponse(
            url="/pages/tests?success=Open question created successfully",
            status_code=303
        )
    except Exception:
        return RedirectResponse(
            url="/pages/tests?error=Failed to create open question",
            status_code=303
        )


@router.post("/pages/tests/create")
def create_test_from_page(
    course_id: int = Form(...),
    title: str = Form(...),
    time_limit: int = Form(...),
    pass_score: int = Form(...),
    max_attempts: int = Form(...),
    question_ids: list[int] = Form(...)
):
    try:
        selected_questions = []
        for question_id in question_ids:
            row = question_repository.get_by_id(question_id)
            if row is None:
                return RedirectResponse(
                    url=f"/pages/tests?error=Question {question_id} not found",
                    status_code=303
                )
            selected_questions.append(question_from_row(row))

        test = test_service.create_test(
            course_id=course_id,
            title=title,
            questions=selected_questions,
            time_limit=time_limit,
            pass_score=pass_score,
            max_attempts=max_attempts,
        )
        test_repository.create(test)
        return RedirectResponse(url="/pages/tests?success=Test created successfully", status_code=303)
    except Exception as error:
        return RedirectResponse(url=f"/pages/tests?error={str(error)}", status_code=303)


@router.get("/pages/profile")
def profile_page(request: Request):
    current_user = get_current_user(request)
    if current_user is None:
        return RedirectResponse(url="/pages/auth?error=Login required", status_code=303)

    profile = ProfileRepository().get(current_user["id"])

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "profile_data": profile,
            "current_user": current_user,
        }
    )


@router.post("/pages/profile/build")
def build_profile_from_page(
    request: Request,
    username: str = Form(...),
    avatar_url: str = Form(""),
    theme: str = Form("light"),
    badge_top_student: str | None = Form(None),
    badge_premium: str | None = Form(None),
    badge_expert: str | None = Form(None)
):
    current_user = get_current_user(request)
    if current_user is None:
        return RedirectResponse(url="/pages/auth?error=Login required", status_code=303)
    user_id = current_user["id"]
    profile = BasicProfile(username)

    if avatar_url.strip():
        profile = AvatarDecorator(profile, avatar_url.strip())

    if theme.strip():
        profile = ThemeDecorator(profile, theme.strip())

    if badge_top_student is not None:
        profile = BadgeDecorator(profile, "Top Student")

    if badge_premium is not None:
        profile = BadgeDecorator(profile, "Premium User")

    if badge_expert is not None:
        profile = BadgeDecorator(profile, "Python Expert")

    profile_data = profile.get_data()
    theme = profile_data["theme"]
    badges = profile_data["badges"]
    command_bus.handle(ChangeThemeCommand(user_id, theme))
    for badge in badges:
        command_bus.handle(AddBadgeCommand(user_id, badge))

    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "profile_data": profile_data,
            "current_user": current_user,
        }
    )


@router.post("/pages/profile/theme")
def change_profile_theme(request: Request, theme: str = Form(...)):
    try:
        current_user = get_current_user(request)
        if current_user is None:
            return RedirectResponse(url="/pages/auth?error=Login required", status_code=303)
        command_bus.handle(ChangeThemeCommand(current_user["id"], theme))
        return RedirectResponse(url="/pages/profile", status_code=303)
    except ValueError as error:
        return RedirectResponse(url=f"/pages/profile?error={str(error)}", status_code=303)


@router.post("/pages/profile/avatar")
def upload_profile_avatar(request: Request, avatar: UploadFile = File(...)):
    current_user = get_current_user(request)
    if current_user is None:
        return RedirectResponse(url="/pages/auth?error=Login required", status_code=303)
    user_id = current_user["id"]
    allowed_extensions = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
    suffix = Path(avatar.filename or "").suffix.lower()
    if suffix not in allowed_extensions:
        return RedirectResponse(url="/pages/profile?error=Unsupported avatar format", status_code=303)

    target_name = f"user_{user_id}_avatar{suffix}"
    target_path = UPLOAD_DIR / target_name
    with target_path.open("wb") as output:
        shutil.copyfileobj(avatar.file, output)

    command_bus.handle(UploadAvatarCommand(user_id, f"/static/uploads/{target_name}"))
    return RedirectResponse(url="/pages/profile", status_code=303)


@router.get("/pages/integration")
def integration_page(request: Request, result: str = ""):
    return templates.TemplateResponse(
        request=request,
        name="integration.html",
        context={
            "result": result,
            "current_user": get_current_user(request),
        }
    )


@router.post("/pages/integration/enroll")
def integration_enroll_from_page(
    request: Request,
    system: str = Form(...),
    student_name: str = Form(...),
    course_name: str = Form(...)
):
    if system == "moodle":
        adapter = MoodleAdapter(MoodleSystem())
    else:
        adapter = GoogleClassroomAdapter(GoogleClassroomSystem())

    result = adapter.enroll(student_name, course_name)

    return templates.TemplateResponse(
        request=request,
        name="integration.html",
        context={
            "result": result,
            "current_user": get_current_user(request),
        }
    )


@router.post("/pages/courses/enroll")
def enroll_course_from_page(request: Request, course_id: int = Form(...)):
    try:
        current_user = get_current_user(request)
        if current_user is None:
            return RedirectResponse(url="/pages/auth?error=Login required", status_code=303)
        user_id = current_user["id"]
        result = learning_facade.enroll_user_to_course(user_id, course_id)
        return RedirectResponse(
            url=f"/pages/courses?success={result['message']}",
            status_code=303,
        )
    except ValueError as error:
        return RedirectResponse(url=f"/pages/courses?error={str(error)}", status_code=303)


@router.get("/pages/dashboard")
def dashboard_page(request: Request):
    current_user = get_current_user(request)
    if current_user is None:
        return RedirectResponse(url="/pages/auth?error=Login required", status_code=303)

    dashboard = learning_facade.dashboard(current_user["id"])
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"dashboard": dashboard, "current_user": current_user},
    )
