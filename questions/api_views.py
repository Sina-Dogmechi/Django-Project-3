from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question
from rest_framework import status
from .serializers import QuestionListSerializer, QuestionDetailSerializer, QuestionCreateSerializer, QuestionUpdateSerializer
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
        question = get_question_by_id(qid=qid)
        self.check_object_permissions(request, question)
        QuestionService.delete_question(question=question)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuestionUpdateView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def patch(self, request, qid):
        question = get_question_by_id(qid=qid)
        self.check_object_permissions(request, question)
        serializer = QuestionUpdateSerializer(instance=question, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(QuestionDetailSerializer(instance=question).data)



