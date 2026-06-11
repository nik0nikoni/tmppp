class TestResult:
    def __init__(self, user_id: int, test_id: int, score: int, max_score: int, passed: bool):
        self.user_id = user_id
        self.test_id = test_id
        self.score = score
        self.max_score = max_score
        self.passed = passed
