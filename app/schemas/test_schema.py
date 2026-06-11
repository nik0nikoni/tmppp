from pydantic import BaseModel
from typing import Any


class MultipleChoiceQuestionCreate(BaseModel):
    question_id: int
    text: str
    difficulty: str
    options: list[str]
    correct_answer: Any
    points: int = 1


class OpenQuestionCreate(BaseModel):
    question_id: int
    text: str
    difficulty: str
    correct_answer: str
    points: int = 1


class TestCreate(BaseModel):
    course_id: int
    title: str
    time_limit: int
    pass_score: int
    max_attempts: int
    question_ids: list[int]


class TestSubmit(BaseModel):
    answers: dict[int, Any]