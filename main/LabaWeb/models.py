from django.db import models

class Note(models.Model):
    """
    модель - простая заметка с заголовком и описанием.
    """
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='notes/', blank=True, null=True)

    def __str__(self):
        return self.title