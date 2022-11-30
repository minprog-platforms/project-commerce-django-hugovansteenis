from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime


class User(AbstractUser):
    pass

class Category(models.Model):
    nameCategory = models.CharField(max_length=45)

    def __str__(self):
        return self.nameCategory


class Bid(models.Model):
    bid = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_bid")

    def __str__(self):
        return f"{self.bid} from {self.user}"


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=350)
    image = models.CharField(max_length=1500)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_bid")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="Category")
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing_comment")
    text = models.CharField(max_length=300)
    date = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user} commented on {self.listing}, {self.date}"
