import json 
from channels.generic.websocket import AsyncWebsocketConsumer 
from django.core.cache import cache

class ServerMetricsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("metrics", self.channel_name)

        cached_metrics = cache.get('latest_metrics')
        if cached_metrics:
            await self.send(text_data=json.dumps(cached_metrics))

        
    async def disconnect(self, code):
        await self.channel_layer.group_discard("metrics",self.channel_name)

    async def send_metrics(self,event):
        metrics = event['metrics']
        await self.send(text_data=json.dumps(metrics))

