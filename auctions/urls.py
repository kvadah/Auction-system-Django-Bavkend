from django.urls import path
from .views import CreateAuctionView,ListAuctionsView,AuctionDetailView,PlaceBidView,HotAuctions,Stats,SaveAuctionsView,SavedAuctionsLisView

urlpatterns = [
    path('',ListAuctionsView.as_view()),
    path('create/',CreateAuctionView.as_view()),
    path('hot_auctions/',HotAuctions.as_view()),
    path('stats/',Stats.as_view()),
    path('<int:id>/',AuctionDetailView.as_view()),
    path('<int:id>/bid/',PlaceBidView.as_view()),
    path('<int:auction_id>/save/',SaveAuctionsView.as_view()),
    path('saved_auctions/',SavedAuctionsLisView.as_view()),
]