from django.urls import path
from . import api_views


app_name = 'questions'
urlpatterns = [
    path('', api_views.AllQuestionsView.as_view()), # endpoint
    path('<uuid:id>/', api_views.QuestionDetailView.as_view()),
    path('create/', api_views.QuestionCreateView.as_view()),
]