from fastapi import APIRouter, HTTPException

from app.domain.entities.test import Test
from app.domain.services.test_service import TestService
from app.repositories.result_repository import ResultRepository
from app.repositories.test_repository import QuestionRepository, TestRepository
from app.schemas.test_schema import (
    MultipleChoiceQuestionCreate,
    OpenQuestionCreate,
    TestCreate,
    TestSubmit,
)


router = APIRouter(prefix="/tests", tags=["Tests"])

test_service = TestService()
question_repository = QuestionRepository()
test_repository = TestRepository()
result_repository = ResultRepository()


def question_from_row(row: dict):
    if row["question_type"] == "MultipleChoiceQuestion":
        return test_service.create_multiple_choice_question(
            question_id=row["id"],
            text=row["text"],
            difficulty=row["difficulty"],
            options=row["options"] or [],
            correct_answer=row["correct_answer"],
            points=row["points"],
        )
    return test_service.create_open_question(
        question_id=row["id"],
        text=row["text"],
        difficulty=row["difficulty"],
        correct_answer=row["correct_answer"],
        points=row["points"],
    )


def test_from_rows(test_row: dict, question_rows: list[dict]) -> Test:
    test = Test()
    test.test_id = test_row["id"]
    test.course_id = test_row["course_id"]
    test.title = test_row["title"]
    test.time_limit = test_row["time_limit"]
    test.pass_score = test_row["pass_score"]
    test.max_attempts = test_row["max_attempts"]
    test.questions = [question_from_row(row) for row in question_rows]
    return test


@router.post("/questions/multiple-choice")
def create_multiple_choice_question(question_data: MultipleChoiceQuestionCreate):
    question = test_service.create_multiple_choice_question(
        question_id=question_data.question_id,
        text=question_data.text,
        difficulty=question_data.difficulty,
        options=question_data.options,
        correct_answer=question_data.correct_answer,
        points=question_data.points,
    )
    question_id = question_repository.create(question)

    return {
        "message": "Multiple choice question created successfully",
        "question_id": question_id,
        "text": question.text,
        "difficulty": question.difficulty,
    }


@router.post("/questions/open")
def create_open_question(question_data: OpenQuestionCreate):
    question = test_service.create_open_question(
        question_id=question_data.question_id,
        text=question_data.text,
        difficulty=question_data.difficulty,
        correct_answer=question_data.correct_answer,
        points=question_data.points,
    )
    question_id = question_repository.create(question)

    return {
        "message": "Open question created successfully",
        "question_id": question_id,
        "text": question.text,
        "difficulty": question.difficulty,
    }


@router.get("/questions")
def get_questions():
    return [
        {
            "question_id": question["id"],
            "text": question["text"],
            "difficulty": question["difficulty"],
            "points": question["points"],
            "type": question["question_type"],
        }
        for question in question_repository.list_all()
    ]


@router.post("/create")
def create_test(test_data: TestCreate):
    selected_questions = []

    for question_id in test_data.question_ids:
        question = question_repository.get_by_id(question_id)
        if question is None:
            raise HTTPException(status_code=404, detail=f"Question with id {question_id} not found")
        selected_questions.append(question_from_row(question))

    test = test_service.create_test(
        course_id=test_data.course_id,
        title=test_data.title,
        questions=selected_questions,
        time_limit=test_data.time_limit,
        pass_score=test_data.pass_score,
        max_attempts=test_data.max_attempts,
    )
    test_id = test_repository.create(test)

    return {
        "message": "Test created successfully",
        "test_id": test_id,
        "title": test.title,
        "course_id": test.course_id,
        "questions_count": len(test.questions),
    }


@router.get("/")
def get_tests():
    return [
        {
            "test_id": test["id"],
            "title": test["title"],
            "course_id": test["course_id"],
            "questions_count": test["questions_count"],
            "time_limit": test["time_limit"],
            "pass_score": test["pass_score"],
            "max_attempts": test["max_attempts"],
        }
        for test in test_repository.list_all()
    ]


@router.post("/{test_id}/submit")
def submit_test(test_id: int, submit_data: TestSubmit, user_id: int = 1):
    bundle = test_repository.get_with_questions(test_id)
    if bundle is None:
        raise HTTPException(status_code=404, detail="Test not found")

    selected_test = test_from_rows(bundle[0], bundle[1])
    result = test_service.submit_test(selected_test, submit_data.answers, user_id=user_id)
    result_repository.create(user_id, test_id, result, submit_data.answers)
    return result


@router.post("/questions/{question_id}/clone")
def clone_question(question_id: int):
    row = question_repository.get_by_id(question_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Question not found")

    question = question_from_row(row)
    cloned = test_service.clone_question_for_test(question)
    cloned.question_id = 0
    new_id = question_repository.create(cloned)

    return {
        "message": "Question cloned successfully",
        "original_id": question_id,
        "new_id": new_id,
    }


@router.get("/questions/select")
def select_questions(strategy: str, student_score: int = 0):
    try:
        questions = [question_from_row(row) for row in question_repository.list_all()]
        selected = test_service.select_questions_by_strategy(questions, strategy, student_score)

        return [
            {
                "question_id": question.question_id,
                "text": question.text,
                "difficulty": question.difficulty,
            }
            for question in selected
        ]
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
