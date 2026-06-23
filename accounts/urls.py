from django.urls import path
from . import api_views
from rest_framework.authtoken import views as token_views


app_name = 'accounts'
urlpatterns = [
    path('register/', api_views.UserRegisterView.as_view()),
    path('api-token-auth/', token_views.obtain_auth_token),
    path('profile/', api_views.UserProfileView.as_view()),
    path('change-password/', api_views.ChangePasswordView.as_view()),
    path('admin/<int:pk>/', api_views.UserDetailView.as_view()),
    path('admin/<int:pk>/deactivate/', api_views.UserDeactivateView.as_view()),
    path('activate/<uidb64>/<token>/', api_views.UserActivationAccountView.as_view()),
]