class Test:
    def __init__(self):
        self.test_id = None
        self.course_id = None
        self.title = ""
        self.questions = []
        self.time_limit = 0
        self.pass_score = 0
        self.max_attempts = 1

    def add_question(self, question) -> None:
        self.questions.append(question)

    def get_total_points(self) -> int:
        total = 0
        for question in self.questions:
            total += question.points
        return total

    def get_info(self) -> str:
        return (
            f"Test(id={self.test_id}, title='{self.title}', "
            f"course_id={self.course_id}, questions={len(self.questions)}, "
            f"time_limit={self.time_limit}, pass_score={self.pass_score}, "
            f"max_attempts={self.max_attempts})"
        )