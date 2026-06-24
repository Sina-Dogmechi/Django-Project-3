from .models import Question


def get_question_by_id(*, qid):
    return Question.objects.get(id=qid)