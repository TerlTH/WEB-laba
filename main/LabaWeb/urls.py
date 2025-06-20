from django.urls import path
from .views import (
    HelloWorldAPIView,
    NoteListCreateAPIView,
    NoteRetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('hello/', HelloWorldAPIView.as_view(), name='hello-world'),
    path('notes/', NoteListCreateAPIView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteRetrieveUpdateDestroyAPIView.as_view(), name='note-detail'),
]
