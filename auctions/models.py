from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64, null=True, default="")

    def __str__(self):
        return f"{self.category}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    start_bid = models.DecimalField(max_digits=1000, decimal_places=2)

    image = models.URLField(blank=True, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, blank=True, null=True
    )
    # One user can have many auctions
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    # Sets field to now when object is created = True -> cannot modify
    created_at = models.DateTimeField(auto_now_add=True)
    # automatically update the date everytime object is saved
    modified_at = models.DateTimeField(auto_now=True)


class Bid(models.Model):
    amount = models.DecimalField(max_digits=1000, decimal_places=2)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bidded_on = models.DateTimeField(auto_now_add=True)
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)


class Comment(models.Model):
    content = models.TextField()
    # CASCADE - When user is deleted comment will be deleted too
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    # Sets field to now when object is created = True -> cannot modify
    created_on = models.DateTimeField(auto_now_add=True)
    lisitng = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
