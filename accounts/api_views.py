from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser



class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data) # Deserializing(json -> python datatype)
        serializer.is_valid(raise_exception=True)
        user = User(email=serializer.validated_data['email'], username=serializer.validated_data['username'])
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)



class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        username = request.data.get('username')
        request.user.username = username
        request.user.save(update_fields=['username'])
        return Response(UserSerializer(request.user).data)



class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save(update_fields=['password'])
        return Response({'message': 'password changed successfully'})


class UserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserDeactivateView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        user = User.objects.filter(id=pk).first()
        if not user:
            return Response({'message': 'user not found'}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response({'message': 'user deactivated'}, status=status.HTTP_200_OK)