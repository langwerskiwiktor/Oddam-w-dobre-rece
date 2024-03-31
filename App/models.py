from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


CHOISES = [
    (1, 'fundacja'),
    (2, 'organizacja pozarządowa'),
    (3, 'zbiórka lokalna')
]


class Institution(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.IntegerField(choices=CHOISES, default=1)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    is_taken = models.BooleanField(default=False, null=True)
