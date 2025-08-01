from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watchlist/<int:listing_id>/",
         views.toggle_watchlist, name="toggle_watchlist"),
    path("watchlist", views.watchlist_view, name="watchlist"),
    path("closed/", views.closed_listings, name="closed_listings"),
    path("categories/", views.categories_view, name="categories"),
    path("categories/<str:category_name>/",
         views.category_listings, name="category_listings"),


]
