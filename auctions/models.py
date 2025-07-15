from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# Category model
class Category(models.Model):
    """This is the category model which inherits from models.Model
        It will be used to create a category table in the database
        for each category created by a user.
    """
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


# Listing model
class Listing(models.Model):
    """This is the listing model which inherits from models.Model
        It will be used to create a listing table in the database
        for each listing created by a user.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="listings")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} (${self.starting_bid})"


# Bid model
class Bid(models.Model):
    """This is the bid model which inherits from models.Model
        It will be used to create a bid table in the database
        for each bid made by a user.
    """
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bid ${self.amount} on {self.listing}"


# Comment model
class Comment(models.Model):
    """This is the comment model which inherits from models.Model
        It will be used to create a comment table in the database
        for each comment made by a user.
    """
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.commenter} on {self.listing}"
