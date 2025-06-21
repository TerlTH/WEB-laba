import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import LabaWeb.routing

# Установка переменной окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

# Главный объект приложения ASGI
application = ProtocolTypeRouter({
    
    # Обработка обычных HTTP-запросов
    "http": get_asgi_application(),

    # Обработка WebSocket с авторизацией
    "websocket": AuthMiddlewareStack(
        URLRouter(
            LabaWeb.routing.websocket_urlpatterns
        )
    ),
})
