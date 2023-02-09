from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newListing", views.newListing, name="newListing"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("categoryFilter", views.categoryFilter, name="categoryFilter"),
    path("archive", views.archive, name="archive"),
    path("showWatchlist", views.showWatchlist, name="showWatchlist"),
    path("addWatchlist/<int:listing_id>", views.addWatchlist, name="addWatchlist"),
    path("removeWatchlist/<int:listing_id>", views.removeWatchlist, name="removeWatchlist"),
    path("newComment/<int:listing_id>", views.newComment, name="newComment"),
    path("receiveBid/<int:listing_id>", views.receiveBid, name="receiveBid"),
    path("closeListing/<int:listing_id>", views.closeListing, name="closeListing"),
    path("myListings", views.myListings, name="myListings"),
]
