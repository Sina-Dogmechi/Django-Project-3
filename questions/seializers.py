from rest_framework import serializers
from questions.models import Question


class QuestionListSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField()
    body = serializers.CharField()
    views_count = serializers.IntegerField()


class QuestionDetailSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username')

    class Meta:
        model = Question
        # fields = '__all__'
        exclude = ('author',)