from django.contrib.gis import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Shop, Review

@admin.register(Shop)
class ShopAdmin(OSMGeoAdmin):
    list_display = ('name','Items_present')

admin.site.register(Review)
