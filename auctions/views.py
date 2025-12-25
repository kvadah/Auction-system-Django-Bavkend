# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import AuctionItem, Bid,SavedAuctions
from .serializers import AuctionItemSerializer, BidSerializer,HotAuctionSerializer
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta


class CreateAuctionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AuctionItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                owner=request.user, current_price=serializer.validated_data['starting_price'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


class ListAuctionsView(APIView):
    def get(self, request):
        items = AuctionItem.objects.filter(
            ends_at__gt=timezone.now()).order_by('-created_at')
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


class HotAuctions(APIView):
    def get(self,request):
        last_24_hours = timezone.now()-timedelta(hours=24)
        hotAuctions = (AuctionItem.objects.
                    filter(bids__created_at__gte=last_24_hours).
                    annotate(last_24h_bids=Count('bids')).
                    order_by('-last_24h_bids')[:5])
        serializer =HotAuctionSerializer(hotAuctions,many=True)
        return Response(serializer.data)

class Stats(APIView):
    def get(self,request):
        last_24_hours=timezone.now()-timedelta(hours=24)

        last_24h_bids=Bid.objects.filter(created_at__gte=last_24_hours).count()
        last_24h_auctions=AuctionItem.objects.filter(created_at__gte=last_24_hours).count()
        total_active_auctions=AuctionItem.objects.filter(ends_at__gt=timezone.now()).count()
        return Response({
            "stats":{
                "last_24h_bids":last_24h_bids,
                "last_24h_auctions":last_24h_auctions,
                "total_active_auctions":total_active_auctions,
            }
        })
    

class SaveAuctionsView(APIView):
    permission_classes =[IsAuthenticated]

    def post(self,request,auction_id):
        auction= get_object_or_404(AuctionItem,id=auction_id)

        saved,created = SavedAuctions.objects.get_or_create(
            auction=auction,
            user=request.user
        )
        if not created:
            return Response ({"auction already saved"})
        
        return Response({"auction saved"})
    def delete(self,request,auction_id):
        auction = get_object_or_404(AuctionItem,auction_id)

        SavedAuctions.objects.filter(
            user=request.user,
            auction=auction
        ).delete()


class SavedAuctionsLisView(APIView):
    permission_classes =[IsAuthenticated]

    def get(self,request):
        saved_auctions = SavedAuctions.objects.filter(user=request.user)
        auctions = [item.auction for item in saved_auctions]
        serialzer = AuctionItemSerializer(auctions,many=True)
        return Response(serialzer.data)