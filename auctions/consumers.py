from channels.generic.websocket import AsyncWebsocketConsumer
import json

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
