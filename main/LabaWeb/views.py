from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework import filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.serializers import ModelSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Note
from .serializers import NoteSerializer


class NoteListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /api/notes/ — список с фильтрацией, поиском, сортировкой
    POST /api/notes/ — создание
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_fields = ['title']              # ?title=...
    search_fields = ['title', 'content']      # ?search=...
    ordering_fields = ['created_at', 'title'] # ?ordering=created_at
    permission_classes = [IsAuthenticatedOrReadOnly]


class NoteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/notes/<id>/ — детали
    PUT/PATCH/DELETE /api/notes/<id>/ — обновление/удаление
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [AllowAny]


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )
        if user is not None:
            login(request, user)
            return Response({"message": "Вы вошли"}, status=status.HTTP_200_OK)
        return Response({"error": "Неверные данные"}, status=status.HTTP_401_UNAUTHORIZED)
    

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Вы вышли"}, status=status.HTTP_200_OK)
    
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"user": request.user.username})
    
class UserListPagination(PageNumberPagination):
    page_size = 5

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    pagination_class = UserListPagination
    permission_classes = [IsAuthenticated]
    

class HelloWorldAPIView(APIView):

    permission_classes = [AllowAny]

    """
    Простейший APIView, поддерживающий методы GET и POST.
    """

    """
    APIView с базовой валидацией данных и кастомным JSON-ответом.
    """

    def get(self, request):
        return Response({
            "status": "success",
            "method": "GET",
            "message": "Добро пожаловать в API!"
        })

    def post(self, request):
        data = request.data

        # Простая ручная валидация
        name = data.get('name')
        if not name:
            return Response(
                {"error": "Поле 'name' обязательно."},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isinstance(name, str):
            return Response(
                {"error": "Поле 'name' должно быть строкой."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Возврат кастомного JSON-ответа
        return Response({
            "status": "created",
            "message": f"Привет, {name}!",
            "length": len(name)
        }, status=status.HTTP_201_CREATED)
    
    