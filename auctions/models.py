from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class AuctionItem(models.Model):
    owner = models.ForeignKey(User,on_delete=models.CASCADE,related_name="auctions")
    title = models.CharField(max_length=255)
    description = models.TextField()
    starting_price= models.DecimalField(max_digits=10,decimal_places=2)
    current_price= models.DecimalField(max_digits=10,decimal_places=2)
    image =models.URLField()
    is_active = models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    ends_at=models.DateTimeField()

    def __str__(self):
        return self.title
    

class Bid(models.Model):
    auction = models.ForeignKey(AuctionItem, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder.username} - {self.amount}"

