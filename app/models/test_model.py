from dataclasses import dataclass


@dataclass
class TestModel:
    id: int
    course_id: int
    title: str
    time_limit: int
    pass_score: int
    max_attempts: int
