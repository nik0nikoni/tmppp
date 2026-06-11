from app.domain.entities.test import Test


class TestBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._test = Test()

    def set_test_id(self, test_id: int):
        self._test.test_id = test_id
        return self

    def set_course_id(self, course_id: int):
        self._test.course_id = course_id
        return self

    def set_title(self, title: str):
        self._test.title = title
        return self

    def add_question(self, question):
        self._test.add_question(question)
        return self

    def set_time_limit(self, time_limit: int):
        self._test.time_limit = time_limit
        return self

    def set_pass_score(self, pass_score: int):
        self._test.pass_score = pass_score
        return self

    def set_max_attempts(self, max_attempts: int):
        self._test.max_attempts = max_attempts
        return self

    def build(self):
        ready_test = self._test
        self.reset()
        return ready_test