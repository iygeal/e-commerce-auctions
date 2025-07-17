from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing

# Import forms
from .forms import RegisterForm, CreateListingForm
from .forms import LoginForm


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
