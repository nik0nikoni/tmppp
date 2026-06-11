from app.domain.patterns.builder import TestBuilder
from app.domain.patterns.abstract_factory import MultipleChoiceFactory, OpenQuestionFactory
from app.domain.patterns.strategy import EasyStrategy, MediumStrategy, HardStrategy, AdaptiveStrategy
from app.domain.patterns.observer import (
    NotificationCenter,
    EmailNotifier,
    SmsNotifier,
    SystemNotifier,
    DatabaseNotifier,
)
from app.repositories.result_repository import NotificationRepository


class TestService:
    def __init__(self):
        self.tests = []
        self.next_id = 1

        self.notification_center = NotificationCenter()
        self.notification_center.attach(EmailNotifier())
        self.notification_center.attach(SmsNotifier())
        self.notification_center.attach(SystemNotifier())

    def create_test(
        self,
        course_id: int,
        title: str,
        questions: list,
        time_limit: int,
        pass_score: int,
        max_attempts: int
    ):
        builder = TestBuilder()

        builder.set_test_id(self.next_id)
        builder.set_course_id(course_id)
        builder.set_title(title)
        builder.set_time_limit(time_limit)
        builder.set_pass_score(pass_score)
        builder.set_max_attempts(max_attempts)

        for question in questions:
            builder.add_question(question)

        test = builder.build()
        self.tests.append(test)
        self.next_id += 1
        return test

    def create_multiple_choice_question(
        self,
        question_id: int,
        text: str,
        difficulty: str,
        options: list,
        correct_answer,
        points: int = 1
    ):
        factory = MultipleChoiceFactory()
        return factory.create_question(
            question_id=question_id,
            text=text,
            difficulty=difficulty,
            data=options,
            correct_answer=correct_answer,
            points=points
        )

    def create_open_question(
        self,
        question_id: int,
        text: str,
        difficulty: str,
        correct_answer: str,
        points: int = 1
    ):
        factory = OpenQuestionFactory()
        return factory.create_question(
            question_id=question_id,
            text=text,
            difficulty=difficulty,
            data=None,
            correct_answer=correct_answer,
            points=points
        )

    def check_answer(self, question, user_answer) -> bool:
        if question.__class__.__name__ == "MultipleChoiceQuestion":
            factory = MultipleChoiceFactory()
        else:
            factory = OpenQuestionFactory()

        checker = factory.create_answer_checker()
        return checker.check_answer(user_answer, question.correct_answer)

    def clone_question_for_test(self, question):
        return question.clone()

    def select_questions_by_strategy(self, questions: list, strategy_type: str, student_score: int = 0):
        if strategy_type == "easy":
            strategy = EasyStrategy()
        elif strategy_type == "medium":
            strategy = MediumStrategy()
        elif strategy_type == "hard":
            strategy = HardStrategy()
        elif strategy_type == "adaptive":
            strategy = AdaptiveStrategy(student_score)
        else:
            raise ValueError("Unknown strategy type")

        return strategy.select_questions(questions)

    def submit_test(self, test, user_answers: dict, user_id: int | None = None):
        total_score = 0
        max_score = test.get_total_points()

        for question in test.questions:
            if question.question_id in user_answers:
                user_answer = user_answers[question.question_id]
                if self.check_answer(question, user_answer):
                    total_score += question.points

        passed = total_score >= test.pass_score
        notification_center = NotificationCenter()
        notification_center.attach(EmailNotifier())
        notification_center.attach(SmsNotifier())
        notification_center.attach(SystemNotifier())
        notification_center.attach(DatabaseNotifier(NotificationRepository(), user_id=user_id))

        if passed:
            notification_center.notify(
                f"Test '{test.title}' successfully passed. Score: {total_score}/{max_score}"
            )
        else:
            notification_center.notify(
                f"Test '{test.title}' failed. Score: {total_score}/{max_score}"
            )

        return {
            "score": total_score,
            "max_score": max_score,
            "passed": passed
        }

    def get_all_tests(self):
        return self.tests
