from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer
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