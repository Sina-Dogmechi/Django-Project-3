from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question
from rest_framework import status
from .seializers import QuestionListSerializer, QuestionDetailSerializer


class AllQuestionsView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serialized_data = QuestionListSerializer(instance=questions, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class QuestionDetailView(APIView):
    def get(self, request, id):
        question = Question.objects.get(id=id)
        serialized_data = QuestionDetailSerializer(instance=question)
        return Response(serialized_data.data, status=status.HTTP_200_OK)