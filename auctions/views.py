from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, Listing

from .models import User


def listing(request, id):
    data_listings= Listing.objects.get(pk=id)
    product_in_watchlist = request.user in data_listings.watchlist.all()
    return render(request, "auctions/listing.html", {
        "listing": data_listings,
        "watchlist": product_in_watchlist
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

        new_listing = Listing(
            title = title,
            description = description,
            image = image,
            price = float(price),
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
