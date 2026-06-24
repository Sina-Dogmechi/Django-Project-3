from .models import Question
from django.db import transaction
from django.db.models import F



class QuestionService:

    @staticmethod
    @transaction.atomic
    def create_question(*, author, title, body):
        question = Question.objects.create(author=author, title=title, body=body)
        return question

    @staticmethod
    def increament_views(*, question):
        # Question.objects.filter(id=question.id).update(views_count=F('views_count') + 1)
        question.views_count = F('views_count') + 1
        question.save()