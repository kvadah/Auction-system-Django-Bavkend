import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import AuctionItem, Bid
from asgiref.sync import sync_to_async

class AuctionConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.auction_id = self.scope['url_route']['kwargs']['auction_id']
        self.room_group_name = f'auction_{self.auction_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Expected payload from frontend:
        {
            "user_id": 1,
            "amount": 600
        }
        """
        data = json.loads(text_data)
        user_id = data['user_id']
        amount = float(data['amount'])

        # Save bid to DB
        bid = await sync_to_async(self.create_bid)(user_id, amount)

        if bid:
            # Broadcast to everyone in the room
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'new_bid',
                    'bidder': bid.bidder.username,
                    'amount': str(bid.amount),
                    'created_at': bid.created_at.isoformat()
                }
            )
        else:
            await self.send(text_data=json.dumps({'error': 'Invalid bid'}))

    # Receive message from room group
    async def new_bid(self, event):
        await self.send(text_data=json.dumps(event))

    def create_bid(self, user_id, amount):
        from django.contrib.auth.models import User
        try:
            auction = AuctionItem.objects.get(id=self.auction_id)
            user = User.objects.get(id=user_id)

            if not auction.is_active or auction.ends_at < timezone.now():
                return None
            if amount <= float(auction.current_price):
                return None

            bid = Bid.objects.create(
                auction=auction,
                bidder=user,
                amount=amount
            )
            auction.current_price = amount
            auction.save()
            return bid
        except:
            return None
