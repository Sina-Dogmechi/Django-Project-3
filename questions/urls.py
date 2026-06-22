from django.urls import path
from . import api_views


app_name = 'questions'
urlpatterns = [
    path('', api_views.AllQuestionsView.as_view(), name='all'), # endpoint
    path('<uuid:id>/', api_views.QuestionDetailView.as_view(), name='detail'),
]