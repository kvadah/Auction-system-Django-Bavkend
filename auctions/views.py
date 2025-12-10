# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import AuctionItem, Bid
from .serializers import AuctionItemSerializer, BidSerializer
from django.shortcuts import get_object_or_404

class CreateAuctionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AuctionItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user, current_price=serializer.validated_data['starting_price'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


class ListAuctionsView(APIView):
    def get(self, request):
        items = AuctionItem.objects.filter(is_active=True).order_by('-created_at')
        serializer = AuctionItemSerializer(items, many=True)
        return Response(serializer.data)


class AuctionDetailView(APIView):
    def get(self, request, id):
        item = get_object_or_404(AuctionItem, id=id)
        serializer = AuctionItemSerializer(item)
        return Response(serializer.data)


class PlaceBidView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        auction = get_object_or_404(AuctionItem, id=id)

        if not auction.is_active:
            return Response({"error": "Auction is not active"}, status=400)

        bid_amount = request.data.get("amount")

        try:
            bid_amount = float(bid_amount)
        except:
            return Response({"error": "Invalid amount"}, status=400)

        if bid_amount <= float(auction.current_price):
            return Response({"error": "Bid must be higher than current price"}, status=400)

        # Save bid
        bid = Bid.objects.create(
            auction=auction,
            bidder=request.user,
            amount=bid_amount
        )

        # Update current price
        auction.current_price = bid_amount
        auction.save()

        serializer = BidSerializer(bid)
        return Response(serializer.data, status=201)
