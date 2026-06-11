class Question:
    def __init__(
        self,
        question_id: int,
        text: str,
        difficulty: str,
        correct_answer,
        points: int = 1
    ):
        self.question_id = question_id
        self.text = text
        self.difficulty = difficulty
        self.correct_answer = correct_answer
        self.points = points

    def display(self) -> str:
        raise NotImplementedError("Method display() must be implemented in subclasses")

    def clone(self):
        raise NotImplementedError("Method clone() must be implemented in subclasses")


class MultipleChoiceQuestion(Question):
    def __init__(
        self,
        question_id: int,
        text: str,
        difficulty: str,
        options: list[str],
        correct_answer,
        points: int = 1
    ):
        super().__init__(question_id, text, difficulty, correct_answer, points)
        self.options = options

    def display(self) -> str:
        options_text = ", ".join(self.options)
        return f"{self.text} | Options: {options_text}"

    def clone(self):
        cloned_options = []
        for option in self.options:
            cloned_options.append(option)

        return MultipleChoiceQuestion(
            question_id=self.question_id,
            text=self.text,
            difficulty=self.difficulty,
            options=cloned_options,
            correct_answer=self.correct_answer,
            points=self.points
        )


class OpenQuestion(Question):
    def __init__(
        self,
        question_id: int,
        text: str,
        difficulty: str,
        correct_answer: str,
        points: int = 1
    ):
        super().__init__(question_id, text, difficulty, correct_answer, points)

    def display(self) -> str:
        return self.text

    def clone(self):
        return OpenQuestion(
            question_id=self.question_id,
            text=self.text,
            difficulty=self.difficulty,
            correct_answer=self.correct_answer,
            points=self.points
        )