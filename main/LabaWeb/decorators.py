from functools import wraps
from django.http import JsonResponse
from .models import Note

def owner_required(view_func):
    """
    Декоратор, проверяющий, что текущий пользователь является владельцем заметки.
    Используется для защиты представлений от несанкционированного доступа.
    
    """
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        note_id = kwargs.get('pk')
        try:
            note = Note.objects.get(pk=note_id)
        except Note.DoesNotExist:
            return JsonResponse({'detail': 'Заметка не найдена'}, status=404)

        if note.owner != request.user:
            return JsonResponse({'detail': 'Доступ запрещён'}, status=403)

        return view_func(self, request, *args, **kwargs)
    return _wrapped_view
