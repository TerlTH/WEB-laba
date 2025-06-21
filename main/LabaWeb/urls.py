from django.urls import path
from rest_framework.routers import DefaultRouter


from .views import (
    HelloWorldAPIView,
    NoteListCreateAPIView,
    NoteRetrieveUpdateDestroyAPIView,
    RegisterView, LoginView, LogoutView,
    ProfileView, UserListView,
    SafeInputView,
    ProductViewSet
)

# Роутер для ViewSet (используется для /api/products/)
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

# Основные пути API
urlpatterns = [
    path('hello/', HelloWorldAPIView.as_view(), name='hello-world'), # Простая проверка
    path('notes/', NoteListCreateAPIView.as_view(), name='note-list-create'), # Список и создание заметок
    path('notes/<int:pk>/', NoteRetrieveUpdateDestroyAPIView.as_view(), name='note-detail'), # Детали, обновление, удаление заметки
]

# Аутентификация и профиль
urlpatterns += [
    path('users/register/', RegisterView.as_view()), # Регистрация
    path('users/login/', LoginView.as_view()), # Вход
    path('users/logout/', LogoutView.as_view()), # Выход
    path('users/profile/', ProfileView.as_view()), # Профиль текущего пользователя
    path('users/list/', UserListView.as_view()), # Список пользователей
] 

# Безопасный ввод
urlpatterns += [
    path('safe/', SafeInputView.as_view()), # Валидация данных (name и age)
]

# Добавляем маршруты из роутера (например, /products/)
urlpatterns += router.urls