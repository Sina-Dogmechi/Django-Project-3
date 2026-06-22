from django.urls import path
from . import api_views


app_name = 'accounts'
urlpatterns = [
    path('register/', api_views.UserRegisterView.as_view()),
]