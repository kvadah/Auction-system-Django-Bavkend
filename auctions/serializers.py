from rest_framework import serializers
from .models import AuctionItem,Bid

class BidSerializer(serializers.ModelSerializer):
    bidder_name = serializers.CharField(source='bidder.username', read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'bidder', 'bidder_name', 'amount', 'created_at']
        read_only_fields = ['id', 'bidder', 'created_at']


class AuctionItemSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.username', read_only=True)
    bids = BidSerializer(many=True, read_only=True)

    class Meta:
        model = AuctionItem
        fields = [
            'id', 'owner', 'owner_name', 'title', 'description', 'starting_price',
            'current_price', 'image', 'is_active', 'created_at', 'ends_at', 'bids'
        ]
        read_only_fields = ['id', 'owner', 'current_price', 'created_at', 'is_active']


class HotAuctionSerializer(serializers.Serializer):
    id=serializers.IntegerField()
    title=serializers.CharField()
    last_24h_bids =serializers.IntegerField()
    image=serializers.ImageField()