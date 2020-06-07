from djgeojson.fields import PointField
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
import decimal
from django.utils import timezone


class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField(null=True,blank=True, spatial_index=True, geography=True)
    lattitude=models.DecimalField(max_digits=20, decimal_places=10,default=decimal.Decimal(0))
    longitude=models.DecimalField(max_digits=20, decimal_places=10,default=decimal.Decimal(0))
    Items_present = ArrayField(models.CharField(max_length=200), blank=True)
    cover_image=models.ImageField(blank=True,null=True,upload_to="covers/%Y/%M/%D")

class Review(models.Model):
    shop = models.ForeignKey('shops.Shop', on_delete=models.CASCADE, related_name='reviews')
    # id = shop.pk
    customer = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_review = models.BooleanField(default=False) 

    def approve(self):
        self.approved_review = True 
        self.save()

    def __str__(self):
        return self.text