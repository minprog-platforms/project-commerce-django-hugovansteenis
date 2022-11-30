from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing, Comment, Bid
import datetime

from .models import User


def stop_bidding(request, id):
    data_listings = Listing.objects.get(pk=id)
    data_listings.is_active = False
    data_listings.save(0)
    is_owner = request.user.username == data_listings.user.username
    product_in_watchlist = request.user in data_listings.watchlist.all()
    all_comments = Comment.objects.filter(listing = data_listings)
    return render(request, "auctions/listing.html", {
        "listing": data_listings,
        "message": "Bidding was stopped, the auction has finished.",
        "watchlist": product_in_watchlist,
        "comments": all_comments,
        "alert": True,
        "is_owner": is_owner
    })


def bid(request, id):
    new_bid = int(request.POST['new_bid'])
    data_listings = Listing.objects.get(pk=id)
    product_in_watchlist = request.user in data_listings.watchlist.all()
    all_comments = Comment.objects.filter(listing = data_listings)
    is_owner = request.user.username == data_listings.user.username
    if new_bid > data_listings.price.bid:
        updated_bid = Bid(user=request.user, bid=new_bid)
        updated_bid.save()
        data_listings.price = updated_bid
        data_listings.save()
        return render(request, "auctions/listing.html", {
            "listing": data_listings,
            "message": "Bid was succesful!",
            "watchlist": product_in_watchlist,
            "comments": all_comments,
            "alert": True,
            "is_owner": is_owner
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": data_listings,
            "message": "Bid failed, your bid was too low.",
            "watchlist": product_in_watchlist,
            "comments": all_comments,
            "alert": True,
            "is_owner": is_owner
        })


def comment(request, id):
    user = request.user
    data_listings = Listing.objects.get(pk=id)
    comment = request.POST['new_comment']

    new_comment = Comment(
        user = user,
        listing = data_listings,
        text = comment,
        date = datetime.date.today()
    )

    new_comment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def listing(request, id):
    data_listings = Listing.objects.get(pk=id)
    product_in_watchlist = request.user in data_listings.watchlist.all()
    all_comments = Comment.objects.filter(listing = data_listings)
    is_owner = request.user.username == data_listings.user.username
    return render(request, "auctions/listing.html", {
        "listing": data_listings,
        "watchlist": product_in_watchlist,
        "comments": all_comments,
        "is_owner": is_owner
    })


def index(request):
    all_active_listings = Listing.objects.filter(is_active = True)
    all_categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": all_active_listings,
        "categories": all_categories
    })


def watchlist(request):
    user = request.user
    all_listings = user.watchlist.all()
    all_categories = Category.objects.all()
    return render(request, "auctions/watchlist.html", {
        "listings": all_listings,
        "categories": all_categories
    })

def watchlistAdd(request, id):
    data_listings= Listing.objects.get(pk=id)
    user = request.user
    data_listings.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def watchlistRemove(request, id):
    data_listings= Listing.objects.get(pk=id)
    user = request.user
    data_listings.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


def categories(request):
    if request.method == "POST":
        form_category = request.POST['category']
        normal_category = Category.objects.get(nameCategory = form_category)
        all_active_listings = Listing.objects.filter(is_active = True, category = normal_category)
        all_categories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": all_active_listings,
            "categories": all_categories
        })


def create_listing(request):
    if request.method == "GET":
        all_categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": all_categories
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        image = request.POST["image"]
        category = request.POST["category"]
        user = request.user

        data_category = Category.objects.get(nameCategory = category)

        bid = Bid(bid=float(price), user=user)
        bid.save()

        new_listing = Listing(
            title = title,
            description = description,
            image = image,
            price = bid,
            category = data_category,
            user = user
        )
        new_listing.save()
        return HttpResponseRedirect(reverse(index))

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
