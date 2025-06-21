import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Product
from asgiref.sync import sync_to_async

class ProductCountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Подключение клиента к группе "products"
        await self.channel_layer.group_add("products", self.channel_name)
        await self.accept()

        # Отправка текущего количества продуктов при подключении
        count = await self.get_product_count()
        await self.send(text_data=json.dumps({"count": count}))

    async def disconnect(self, close_code):
        # Отключение клиента от группы
        await self.channel_layer.group_discard("products", self.channel_name)

    async def product_update(self, event):
        # Отправка обновлённого количества продуктов при изменениях
        await self.send(text_data=json.dumps({"count": event["count"]}))

    @staticmethod
    async def get_product_count():
        # Получение количества продуктов из базы данных
        return await sync_to_async(Product.objects.count)()

