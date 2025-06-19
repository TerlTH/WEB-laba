from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class HelloWorldAPIView(APIView):
    """
    Простейший APIView, поддерживающий методы GET и POST.
    """

    def get(self, request):
        """
        Обработка GET-запроса.
        Возвращает простой JSON-ответ.
        """
        return Response({"message": "GET-запрос получен успешно"}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Обработка POST-запроса.
        Возвращает данные, полученные от клиента.
        """
        data = request.data  # Получаем данные из тела запроса
        return Response({"message": "POST-запрос получен", "data": data}, status=status.HTTP_201_CREATED)
