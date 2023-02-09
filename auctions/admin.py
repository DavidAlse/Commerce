from django.contrib import admin

from .models import User, Category, auctionListing, Bid, Comment

# Register your models here.
admin.site.register(auctionListing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(User)