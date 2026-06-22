from django.db import models
from core.models import BaseModel
from django.conf import settings


class Answer(BaseModel):
    question = models.ForeignKey('questions.Question', on_delete=models.CASCADE, related_name='answers')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_answers')
    body = models.TextField()
    is_accepted = models.BooleanField(default=False)
    score = models.IntegerField(default=0)

    class Meta:
        ordering = ('-is_accepted', '-score', '-created')

    def __str__(self):
        return f"Answer #{self.pk}"