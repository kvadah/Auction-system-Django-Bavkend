
from django.urls import path
from auctions.consumers import AuctionConsumer
from notifications.consumers import NotificationConsumer
websocket_urlpatterns = [
    path('ws/auction/<int:auction_id>/',AuctionConsumer.as_asgi()),
    path('ws/notifications/<int:user_id>/',NotificationConsumer.as_asgi())
]