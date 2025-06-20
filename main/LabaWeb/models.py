from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    """
    модель - простая заметка с заголовком и описанием.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='notes/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.title