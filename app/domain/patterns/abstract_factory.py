from app.domain.entities.question import MultipleChoiceQuestion, OpenQuestion


class AnswerChecker:
    def check_answer(self, user_answer, correct_answer) -> bool:
        raise NotImplementedError("Method check_answer() must be implemented in subclasses")


class MultipleChoiceAnswerChecker(AnswerChecker):
    def check_answer(self, user_answer, correct_answer) -> bool:
        return user_answer == correct_answer


class OpenQuestionAnswerChecker(AnswerChecker):
    def check_answer(self, user_answer, correct_answer) -> bool:
        if not isinstance(user_answer, str) or not isinstance(correct_answer, str):
            return False
        return user_answer.strip().lower() == correct_answer.strip().lower()


class QuestionFactory:
    def create_question(self, question_id: int, text: str, difficulty: str, data, correct_answer, points: int = 1):
        raise NotImplementedError("Method create_question() must be implemented in subclasses")

    def create_answer_checker(self) -> AnswerChecker:
        raise NotImplementedError("Method create_answer_checker() must be implemented in subclasses")


class MultipleChoiceFactory(QuestionFactory):
    def create_question(
        self,
        question_id: int,
        text: str,
        difficulty: str,
        data,
        correct_answer,
        points: int = 1
    ):
        return MultipleChoiceQuestion(
            question_id=question_id,
            text=text,
            difficulty=difficulty,
            options=data,
            correct_answer=correct_answer,
            points=points
        )

    def create_answer_checker(self) -> AnswerChecker:
        return MultipleChoiceAnswerChecker()


class OpenQuestionFactory(QuestionFactory):
    def create_question(
        self,
        question_id: int,
        text: str,
        difficulty: str,
        data,
        correct_answer,
        points: int = 1
    ):
        return OpenQuestion(
            question_id=question_id,
            text=text,
            difficulty=difficulty,
            correct_answer=correct_answer,
            points=points
        )

    def create_answer_checker(self) -> AnswerChecker:
        return OpenQuestionAnswerChecker()