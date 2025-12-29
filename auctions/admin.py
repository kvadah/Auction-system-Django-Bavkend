from django.contrib import admin
from .models import AuctionItem
from .models import Bid
admin.site.register(AuctionItem)
admin.site.register(Bid)
# Register your models here.
