from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question
from rest_framework import status
from .serializers import QuestionListSerializer, QuestionDetailSerializer, QuestionCreateSerializer
from rest_framework.permissions import IsAuthenticated
from .services import QuestionService
from core.permissions import IsOwnerOrReadOnly
from .selectors import get_question_by_id


class AllQuestionsView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serialized_data = QuestionListSerializer(instance=questions, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class QuestionDetailView(APIView):
    def get(self, request, id):
        question = Question.objects.get(id=id)
        serialized_data = QuestionDetailSerializer(instance=question)
        QuestionService.increament_views(question=question)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class QuestionCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = QuestionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question = QuestionService.create_question(author=request.user, title=serializer.validated_data['title'], body=serializer.validated_data['body'])
        return Response(QuestionDetailSerializer(question).data, status=status.HTTP_201_CREATED)


class QuestionDeleteView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def delete(self, request, qid):
        qs = get_question_by_id(qid=qid)
        self.check_object_permissions(request, qs)
        QuestionService.delete_question(question=qs)
        return Response(status=status.HTTP_204_NO_CONTENT)






