from tkinter import NONE
from unicodedata import category, name
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    pass

#our application should have at least three models in addition to the User model: one for auction listings, one for bids, and one for comments made on auction listings.
class Category(models.Model):
    categoryName = models.CharField(max_length=50)

    def __str__(self):
        return self.categoryName

class Bid(models.Model):
    newBid = models.DecimalField(default=0, max_digits=11, decimal_places=2)
    bidTime = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="bidder")

    def __str__(self):
        return f"${self.newBid}"

class auctionListing(models.Model):
    Title = models.CharField(max_length=120)
    Description = models.CharField(max_length=500)
    Image = models.URLField(max_length=500, blank=True)
    isActive = models.BooleanField(default=True)

    NOCATEGORY = 'None'
    TECHNOLOGY = 'Tech'
    FASHION = 'Fashion'
    AUTOMOTIVE = 'Automotive'
    TOOLS = 'Tools'
    MEDIA = 'Media'
    CATEGORY_CHOICES = [
        (NOCATEGORY, 'None'),
        (TECHNOLOGY, 'Technology'),
        (FASHION, 'Fashion'),
        (AUTOMOTIVE, 'Automotive'),
        (TOOLS, 'Tools'),
        (MEDIA, 'Media'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    ##Category = models.CharField(
       # max_length=30,
        
       # choices = CATEGORY_CHOICES,
       # default = NOCATEGORY,
    #)
    
    starting_Bid = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    createdAt = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField(auto_now=True)
    currentBid = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="bid")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watching")

    def __str__(self):
        #return f"{self.Title} has a starting bid of ${self.starting_Bid}"
        return self.Title

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="commenter")
    listing = models.ForeignKey(auctionListing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    commentText = models.CharField(max_length=200)
    posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commenter} commented on {self.listing}"