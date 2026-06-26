from rest_framework.views import APIView
from rest_framework.response import Response
from questions.selectors import get_question_by_id
from .selectors import get_answers_for_question
from .serializers import AnswersListSerializer


class AnswersListView(APIView):
    def get(self, request, question_id):
        question = get_question_by_id(qid=question_id)
        answers = get_answers_for_question(question=question)
        serializer = AnswersListSerializer(instance=answers, many=True)
        return Response(serializer.data)