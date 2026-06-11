class QuestionSelectionStrategy:
    def select_questions(self, questions: list):
        raise NotImplementedError("Method select_questions() must be implemented in subclasses")


class EasyStrategy(QuestionSelectionStrategy):
    def select_questions(self, questions: list):
        selected = []
        for question in questions:
            if question.difficulty == "easy":
                selected.append(question)
        return selected


class MediumStrategy(QuestionSelectionStrategy):
    def select_questions(self, questions: list):
        selected = []
        for question in questions:
            if question.difficulty == "medium":
                selected.append(question)
        return selected


class HardStrategy(QuestionSelectionStrategy):
    def select_questions(self, questions: list):
        selected = []
        for question in questions:
            if question.difficulty == "hard":
                selected.append(question)
        return selected


class AdaptiveStrategy(QuestionSelectionStrategy):
    def __init__(self, student_score: int):
        self.student_score = student_score

    def select_questions(self, questions: list):
        if self.student_score < 50:
            target_difficulty = "easy"
        elif self.student_score < 80:
            target_difficulty = "medium"
        else:
            target_difficulty = "hard"

        selected = []
        for question in questions:
            if question.difficulty == target_difficulty:
                selected.append(question)

        return selected