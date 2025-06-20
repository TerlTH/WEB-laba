from django.urls import path
from .views import (
    HelloWorldAPIView,
    NoteListCreateAPIView,
    NoteRetrieveUpdateDestroyAPIView,
    RegisterView, LoginView, LogoutView,
    ProfileView, UserListView,
    SafeInputView
)

urlpatterns = [
    path('hello/', HelloWorldAPIView.as_view(), name='hello-world'),
    path('notes/', NoteListCreateAPIView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteRetrieveUpdateDestroyAPIView.as_view(), name='note-detail'),
]

urlpatterns += [
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/logout/', LogoutView.as_view()),
    path('users/profile/', ProfileView.as_view()),
    path('users/list/', UserListView.as_view()),
]

urlpatterns += [
    path('safe/', SafeInputView.as_view()),
]
