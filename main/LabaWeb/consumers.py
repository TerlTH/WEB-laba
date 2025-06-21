import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Product

class ProductCountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("products", self.channel_name)
        await self.accept()

        count = await self.get_product_count()
        await self.send(text_data=json.dumps({"count": count}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("products", self.channel_name)

    async def product_update(self, event):
        await self.send(text_data=json.dumps({"count": event["count"]}))

    @staticmethod
    async def get_product_count():
        return await sync_to_async(Product.objects.count)()

from asgiref.sync import sync_to_async