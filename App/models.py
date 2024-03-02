from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)


class Institution(models.Model):
    FUNDACJA = 'fundacja'
    ORGANIZACJA_POZARZĄDOWA = 'organizacja_pozarzadowa'
    ZBIÓRKA_LOKALNA = 'zbiorka_lokalna'

    TYPE_CHOICES = [
        (FUNDACJA, 'Fundacja'),
        (ORGANIZACJA_POZARZĄDOWA, 'Organizacja pozarządowa'),
        (ZBIÓRKA_LOKALNA, 'Zbiórka lokalna'),
    ]

    name = models.CharField(max_length=256)
    description = models.TextField()
    type = models.CharField(max_length=100, choices=TYPE_CHOICES, default=FUNDACJA)
    category = models.ManyToManyField(Category)


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

