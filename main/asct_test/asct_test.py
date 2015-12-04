__author__ = 'Alexey Kutepov'

from enum import Enum


class Answer():
    """
    The Open answer
    """

    def __init__(self, correct_answer):
        self._correct_answer = correct_answer

    def set_answer(self, correct_answer):
        self._correct_answer = correct_answer

    def get_answer(self):
        return self._correct_answer


class CloseAnswer(Answer):
    """
    The close answer
    """

    def __init__(self, answer, is_correct):
        super().__init__(answer)
        self._is_correct = is_correct

    def set_is_correct(self, is_correct):
        self._is_correct = is_correct

    def is_correct(self):
        return self._is_correct


class TestType(Enum):
    """
    Test type constants:
    """
    CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS = 1
    CLOSE_TYPE_ONE_CORRECT_ANSWER = 2
    OPEN_TYPE = 3


class Question:
    """
    This is structure of the question
    """

    def __init__(self, question, test_type=TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS):
        self._question = question
        self._image = None
        self._test_type = test_type
        self._answer = None
        self._correct_count = 0

    def set_question(self, question):
        self._question = question

    def get_question(self):
        return self._question

    def set_image(self, image):
        self._image = image

    def get_image(self):
        return self._image

    def get_test_type(self):
        return self._test_type

    def add_new_answer(self, answer):
        if self._test_type is TestType.OPEN_TYPE:
            if not isinstance(answer, Answer):
                raise AttributeError("The attribute 'answer' is not instance of Answer class")
            else:
                self._answer = answer
        elif self._test_type is TestType.CLOSE_TYPE_ONE_CORRECT_ANSWER:
            if not isinstance(answer, CloseAnswer):
                raise AttributeError("The attribute 'answer' is not instance of CloseAnswer class")
            else:
                if self._answer is None:
                    self._answer = []
                if answer.is_correct():
                    if self._correct_count > 0:
                        raise AttributeError("The correct answer must be only one!")
                    else:
                        self._correct_count += 1
                self._answer.append(answer)
        elif self._test_type is TestType.CLOSE_TYPE_SEVERAL_CORRECT_ANSWERS:
            if not isinstance(answer, CloseAnswer):
                raise AttributeError("The attribute 'answer' is not instance of CloseAnswer class")
            else:
                if self._answer is None:
                    self._answer = []
                self._answer.append(answer)
                self._correct_count += 1

    def get_answers(self):
        return self._answer

    def get_correct_count(self):
        return self._correct_count


class AsctTest:
    """
    There is a list of Questions.
    """

    def __init__(self):
        self._questions = []

    def add_question(self, question):
        """
        Add a new question into the list
        :param question: new question
        """
        if not isinstance(question, Question):
            raise AttributeError("The attribute 'question' is not instance of Question class")
        self._questions.append(question)

    def get_questions(self):
        return self._questions


class AsctResult:
    """
    The result of the question answer
    """

    def __init__(self, is_correct, answer):
        self._is_correct = is_correct
        self._answer = answer

    def is_correct(self):
        return self._is_correct

    def get_answer(self):
        return self._answer

    def set_is_correct(self, is_correct):
        self._is_correct = is_correct

    def set_answer(self, answer):
        self._is_correct = answer