from django.urls import path
from .views import HelloWorldAPIView, NoteAPIView

urlpatterns = [
    path('hello/', HelloWorldAPIView.as_view(), name='hello-world'),
    path('notes/', NoteAPIView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', NoteAPIView.as_view(), name='note-detail'),
]
