from subject.models import TestQuestion


def calculate_test_ball(level, question_ball):
    total_ball = 0
    if level == TestQuestion.QuestionLevel.EASY:
        return total_ball + question_ball
    elif level == TestQuestion.QuestionLevel.MEDIUM:
        return total_ball + question_ball + 1
    else:
        return total_ball + question_ball + 2
