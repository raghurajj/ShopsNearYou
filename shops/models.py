from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
import decimal

class Shop(models.Model):
    name = models.CharField(max_length=100)
    location = models.PointField(null=True, spatial_index=True, geography=True,srid=4326)
    lattitude=models.DecimalField(max_digits=20, decimal_places=10,default=decimal.Decimal(0))
    longitude=models.DecimalField(max_digits=20, decimal_places=10,default=decimal.Decimal(0))
    Items_present = ArrayField(models.CharField(max_length=200), blank=True)
    cover_image=models.ImageField(blank=True,null=True,upload_to="covers/%Y/%M/%D")
    
 