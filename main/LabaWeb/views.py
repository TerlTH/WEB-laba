from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from .models import Note
from .serializers import NoteSerializer


class NoteAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk=None):
        """
        GET /api/notes/ — список
        GET /api/notes/<id>/ — одна запись
        """
        if pk:
            note = get_object_or_404(Note, pk=pk)
            serializer = NoteSerializer(note)
            return Response(serializer.data)
        else:
            notes = Note.objects.all()
            serializer = NoteSerializer(notes, many=True)
            return Response(serializer.data)

    def post(self, request):
        """
        POST /api/notes/ — создание записи
        """
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """
        PUT /api/notes/<id>/ — полное обновление
        """
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """
        PATCH /api/notes/<id>/ — частичное обновление
        """
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteSerializer(note, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        DELETE /api/notes/<id>/ — удаление
        """
        note = get_object_or_404(Note, pk=pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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