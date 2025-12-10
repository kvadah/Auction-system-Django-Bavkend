from django.urls import path
from .views import CreateAuctionView,ListAuctionsView,AuctionDetailView,PlaceBidView

urlpatterns = [
    path('',ListAuctionsView.as_view()),
    path('create/',CreateAuctionView.as_view()),
    path('<int:id>/',AuctionDetailView.as_view()),
    path('<int:id>/bid/',PlaceBidView.as_view()),
]