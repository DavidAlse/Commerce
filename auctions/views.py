from pickle import FALSE
import re
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .forms import auctionListingForm, newBidForm
from crispy_forms.helper import FormHelper
from .models import auctionListing, Bid, Category, User, Comment
from django.core.paginator import Paginator

#The styling of forms can be done by creating a class here, or by doing this in a forms.py file
class newEntryForm(forms.Form):
    entryTite = forms.CharField(widget=forms.TextInput(attrs={'id' : 'newEntryTitle','placeholder': 'Title', 'class': 'form-control', 'autofill': FALSE}))
    entryText = forms.CharField(widget=forms.Textarea(attrs={'id' : 'newEntryText', 'placeholder': 'Your text here', 'class': 'form-control', 'autofill': FALSE}))


def index(request):
    activeListings = auctionListing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
     #activeListings = auctionListing.objects.all().order_by('auctionListing.Title').values()
    p = Paginator(activeListings, 12)

    page_number = request.GET.get('page')
    listingPage = p.get_page(page_number)
    #totalNumPages = "a" * listingPage.paginator.num_pages
    return render(request, "auctions/index.html", {
        'listings': activeListings,
        'listingPage': listingPage,
        'categories': allCategories
        #'totalNumPages': totalNumPages
    })

def myListings(request):
    currentUser = request.user
    ownedListings = auctionListing.objects.filter(owner=currentUser)
    
     #activeListings = auctionListing.objects.all().order_by('auctionListing.Title').values()
    p = Paginator(ownedListings, 12)

    page_number = request.GET.get('page')
    listingPage = p.get_page(page_number)
    #totalNumPages = "a" * listingPage.paginator.num_pages
    return render(request, "auctions/myListings.html", {
        'listingPage': listingPage,
        'ownedListings': ownedListings
        #'totalNumPages': totalNumPages
    })

def categoryFilter(request):
    if request.method == "POST":
        categorySelected = True
        categoryChosen = request.POST["category"]
        category = Category.objects.get(categoryName=categoryChosen)
        activeListings = auctionListing.objects.filter(isActive=True, Category=category)
        allCategories = Category.objects.all()
        #activeListings = auctionListing.objects.all().order_by('auctionListing.Title').values()
        p = Paginator(activeListings, 12)

        page_number = request.GET.get('page')
        listingPage = p.get_page(page_number)
        #totalNumPages = "a" * listingPage.paginator.num_pages
        return render(request, "auctions/index.html", {
            'listings': activeListings,
            'listingPage': listingPage,
            'categories': allCategories,
            'categorySelected': categorySelected
            #'totalNumPages': totalNumPages
    })

def archive(request):
    inactiveListings = auctionListing.objects.filter(isActive=False)
    allCategories = Category.objects.all()
     #activeListings = auctionListing.objects.all().order_by('auctionListing.Title').values()
    p = Paginator(inactiveListings, 12)

    page_number = request.GET.get('page')
    listingPage = p.get_page(page_number)
    #totalNumPages = "a" * listingPage.paginator.num_pages
    return render(request, "auctions/archive.html", {
        'listings': inactiveListings,
        'listingPage': listingPage,
        'categories': allCategories
        #'totalNumPages': totalNumPages
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def newListing(request):
    
    if request.method == "POST":
        currentUser = request.user
        f = auctionListingForm(request.POST)
        if f.is_valid():
            post = f.save(commit=False)
            post.owner = currentUser
            bid = Bid(newBid=float(post.starting_Bid), bidder=currentUser)
            bid.save()
            post.currentBid=bid
            f.save()
            
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/newListing.html", {
            "form": f
    })
    else:
        return render(request, "auctions/newListing.html", {
            "form": auctionListingForm,      
    })

def listing(request, listing_id):
    listing = auctionListing.objects.get(pk=listing_id)
    isActive = listing.isActive
    #bid = Bid.objects.get(pk=listing_id)
    #currentBid = Bid.objects.latest('bidTime') <- gets latest bid out of all listings
    isWatched = request.user in listing.watchlist.all()
    allComments = Comment.objects.filter(listing=listing_id)
    isOwner = False
    if listing.owner == request.user:
        isOwner = True
    
    #if request.method == "POST":
        #receiveBid(request, listing_id)
        #return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))
        
    #else:
        
    return render(request, "auctions/listing.html", {
    "listing": listing,
    "form": newBidForm,
    "currentBid": listing.currentBid,
    "isWatched": isWatched,
    "allComments": allComments,
    "isOwner": isOwner,
    "isActive": isActive
    #"bid": bid
    })

def showWatchlist(request):
    currentUser = request.user
    watching = currentUser.watching.all()
    allCategories = Category.objects.all()
    
    p = Paginator(watching, 12)

    page_number = request.GET.get('page')
    listingPage = p.get_page(page_number)
    return render(request, "auctions/watchlist.html", {
        "watching": watching,
        'categories': allCategories,
        "listingPage": listingPage,
        "currentUser": currentUser
    })


def addWatchlist(request, listing_id):
    listing = auctionListing.objects.get(pk=listing_id)
    currentUser = request.user
    listing.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

def removeWatchlist(request, listing_id):
    listing = auctionListing.objects.get(pk=listing_id)
    currentUser = request.user
    listing.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

def newComment(request, listing_id):
    listing = auctionListing.objects.get(pk=listing_id)
    currentUser = request.user
    commentText = request.POST['newComment']
    #if form.is_valid():
    newComment = Comment(
        listing=listing,
        commenter=currentUser,
        commentText=commentText
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}))

def receiveBid(request, listing_id):
    listing = auctionListing.objects.get(pk=listing_id)
    isActive = listing.isActive
    newBid = float(request.POST['newBid'])
    currentUser = request.user
    isWatched = request.user in listing.watchlist.all()
    allComments = Comment.objects.filter(listing=listing_id)
    isOwner = False
    if listing.owner == request.user:
        isOwner = True
    #post.currentBid=bid
    if newBid > listing.currentBid.newBid:
        receiveBid = Bid(
        bidder=currentUser,
        newBid=newBid
        )
        receiveBid.save()
        listing.currentBid = receiveBid
        listing.save()
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Bid submitted succesfully",
            "success": True,
            "isWatched": isWatched,
            "allComments": allComments,
            "isOwner": isOwner,
            "isActive": isActive
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Bid amount must be higher than Current Bid!",
            "success": False,
            "isWatched": isWatched,
            "allComments": allComments,
            "isOwner": isOwner,
            "isActive": isActive
        })

    
def closeListing(request, listing_id):
    
    listing = auctionListing.objects.get(pk=listing_id)
    listing.isActive = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", kwargs={'listing_id': listing_id}), {
    })
    
     