from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .services import create_user, update_profile, change_password, deactivate_user, build_reset_password_link, send_reset_password_email
from .selectors import get_user_by_id, get_user_by_email
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from .models import User



class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data) # Deserializing(json -> python datatype)
        serializer.is_valid(raise_exception=True)
        user = create_user(email=serializer.validated_data['email'], username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        username = request.data.get('username')
        user = update_profile(user=request.user, username=username)
        return Response(UserSerializer(user).data)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_password(user=request.user, new_password=serializer.validated_data['password'])
        return Response({'message': 'password changed successfully'})


class UserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDeactivateView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        user = get_user_by_id(pk)
        if not user:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        deactivate_user(user=user)
        return Response({'message': 'user deactivated'}, status=status.HTTP_200_OK)


class UserActivationAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'message':'Invalid Link'}, status=status.HTTP_400_BAD_REQUEST)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save(update_fields=['is_active'])
            return Response({'message': 'User activated'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid Link'}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_by_email(serializer.validated_data['email'])

        if user:
            reset_url = build_reset_password_link(user)
            send_reset_password_email(user=user, reset_url=reset_url)
        return Response({"message": "a reset link has been sent."})


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_user_by_id(user_id=uid)
        except Exception:
            return Response({'message': 'Invalid Link'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'message': 'Invalid Link'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])
        return Response({'message': 'password changed successfully'})






















