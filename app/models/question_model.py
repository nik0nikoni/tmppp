from dataclasses import dataclass


@dataclass
class QuestionModel:
    id: int
    question_type: str
    text: str
    difficulty: str
    correct_answer: str
    points: int
