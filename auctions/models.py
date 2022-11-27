from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    nameCategory = models.CharField(max_length=45)

    def __str__(self):
        return self.nameCategory

class Listing(models.Model):
    title = models.CharField(max_length=35)
    description = models.CharField(max_length=350)
    image = models.CharField(max_length=1500)
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="Category")

    def __str__(self):
        return self.title
