from django.urls import path
from .consumers import ProductCountConsumer

websocket_urlpatterns = [
    path("ws/products/count/", ProductCountConsumer.as_asgi()),
]