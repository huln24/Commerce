from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, AuctionListing, Bid, Category, Comment


def index(request):
    return render(
        request, "auctions/index.html", {"listings": AuctionListing.objects.all()}
    )


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


# Display current user's watchlist
@login_required
def watchlist(request):
    pass


# Place for creating new lisitng (only for logged in user)
@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        start_bid = request.POST["start_bid"]
        image_url = request.POST["image"]
        category = request.POST.get("category")
        current_user = request.user
        l = AuctionListing.objects.create(
            title=title,
            description=description,
            start_bid=start_bid,
            image=image_url,
            category=category,
            creator=current_user,
        )
        l.save()
        return redirect(listing, l.id, l.title)
    else:
        return render(
            request,
            "auctions/create_listing.html",
            {"categories": Category.objects.all()},
        )


# List all categories, clicking on category name
# redirects user to list of active listings in that category
def categories(request):
    return render(
        request,
        "auctions/categories.html",
        {
            "categories": Category.objects.all(),
            "no_category": AuctionListing.objects.filter(category__isnull=True).count(),
        },
    )


def category(request, category):
    # If no category, filters all lisings with null category and lists all listings without Category
    if category == "Other":
        return render(
            request,
            "auctions/category_page.html",
            {
                "listings": AuctionListing.objects.filter(category__isnull=True),
                "category": category,
            },
        )
    else:
        category_id = Category.objects.get(category=category).id
        return render(
            request,
            "auctions/category_page.html",
            {
                "listings": AuctionListing.objects.filter(category=category_id),
                "category": category,
            },
        )


def listing(request, id, title):
    return render(
        request, "auctions/listing.html", {"listing": AuctionListing.objects.get(id=id)}
    )
