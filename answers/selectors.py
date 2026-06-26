from .models import Answer


def get_answers_for_question(*, question):
    return Answer.objects.filter(question=question)