from .models import Question
from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import PermissionDenied, ValidationError



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

    @staticmethod
    @transaction.atomic
    def delete_question(*, question):
        question.delete()

    @staticmethod
    @transaction.atomic
    def accepted_answer(*, question, answer, accepted_by):
        if question.author.id != accepted_by.id:
            raise PermissionDenied("only question owner can accept answer")

        if answer.question.id != question.id:
            raise ValidationError("answer does not belong to question")

        if question.accepted_answer:
            raise ValidationError("question already hsa accepted answer")

        question.accepted_answer = answer
        question.save(update_fields=["accepted_answer"])
        answer.is_accepted = True
        answer.save(update_fields=["is_accepted"])
        return question