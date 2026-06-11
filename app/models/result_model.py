from dataclasses import dataclass


@dataclass
class ResultModel:
    id: int
    user_id: int
    test_id: int
    score: int
    max_score: int
    passed: bool
