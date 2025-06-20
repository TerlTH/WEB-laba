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
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import serializers

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Note
from .serializers import NoteSerializer

class SafeInputView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        name = request.data.get('name')
        age = request.data.get('age')

        # Валидация имени
        if not name or not isinstance(name, str):
            return Response({'error': 'Поле \"name\" обязательно и должно быть строкой'}, status=400)

        # Валидация возраста
        if age:
            try:
                age = int(age)
            except ValueError:
                return Response({'error': 'Поле \"age\" должно быть числом'}, status=400)

        return Response({
            'message': 'Данные приняты',
            'name': name.strip(),
            'age': age
        })
    

class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Файл обязателен'}, status=400)

        return Response({
            'filename': file.name,
            'size': file.size
        })


class NoteListCreateAPIView(generics.ListCreateAPIView):
    """
    GET /api/notes/ — список с фильтрацией, поиском, сортировкой
    POST /api/notes/ — создание
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

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
    parser_classes = [MultiPartParser, FormParser]

class UserRegisterSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'age')

    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("Регистрация доступна только с 18 лет.")
        return value

    def create(self, validated_data):
        validated_data.pop('age')  # убираем, чтобы не ушло в User.create_user
        return User.objects.create_user(**validated_data)
    

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
    

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
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
    
    