from .models import Listing
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listing, Bid

# Import forms
from .forms import (
    RegisterForm, CreateListingForm,
    LoginForm, BidForm
)


def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, "auctions/login.html", {
        "form": form
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            login(request, user)
            return redirect("index")
        else:
            return render(request, "auctions/register.html", {
                "form": form
            })
    else:
        form = RegisterForm()
        return render(request, "auctions/register.html", {
            "form": form
        })


@login_required
def create_listing(request):
    """
    Handle the creation of a new listing.

    This view requires the user to be authenticated. If the request method is
    POST, it processes the submitted form data to create a new listing. The
    current user is set as the owner of the listing. Upon successful creation,
    the user is redirected to the index page. If the request method is GET, it
    renders the create listing page with an empty form.
    """

    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  # Set the current user as the owner
            listing.save()
            return redirect('index')
    else:
        form = CreateListingForm()

    return render(request, "auctions/create_listing.html", {
        "form": form
    })


def listing(request, listing_id):
    """
    Handle a request to view a specific listing.

    This view requires the user to be authenticated. The view takes a listing
    ID as an argument. If the listing does not exist, a 404 error is raised.
    Otherwise, the view renders the listing page with the listing object
    passed as context.
    """
    listing = get_object_or_404(Listing, pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing": listing
    })


@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
    else:
        request.user.watchlist.add(listing)

    return redirect("listing", listing_id=listing_id)


@login_required
def watchlist_view(request):
    """
    Handle a request to view a user's watchlist.

    This view requires the user to be authenticated. The view takes no arguments.
    The view renders the watchlist page with the user's watchlist items
    passed as context.
    """
    user = request.user

    watchlist_items = user.watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist_items
    })


def listing_view(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    is_watched = request.user.is_authenticated and request.user.watchlist.filter(
        pk=listing.pk).exists()

    current_bid = listing.bids.order_by('-amount').first()
    current_price = current_bid.amount if current_bid else listing.starting_bid

    bid_form = BidForm()

    if request.method == 'POST' and 'place_bid' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')

        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            new_bid = bid_form.cleaned_data['amount']
            if new_bid > current_price:
                Bid.objects.create(
                    listing=listing,
                    bidder=request.user,
                    amount=new_bid
                )
                messages.success(request, "Bid placed successfully!")
                return redirect('listing', listing_id=listing.id)
            else:
                messages.error(
                    request, f"Your bid must be higher than the current price (${current_price}).")

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_price": current_price,
        "is_watched": is_watched,
        "bid_form": bid_form,
        "current_bidder": current_bid.bidder if current_bid else None,
    })
