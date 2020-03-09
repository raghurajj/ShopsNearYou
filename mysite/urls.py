
import sys
sys.path.append("..")

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from shops import views
from django.conf import settings
from django.views.static import serve
from djgeojson.views import GeoJSONLayerView
from shops.models import Shop



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home.as_view(),name='home'),
    path('shop/new/', views.shop_new, name='shop_new'),
]




if settings.DEBUG:
    urlpatterns+=[
        url(r'^media/(?P<path>.*)$',serve,{
            'document_root':settings.MEDIA_ROOT
        }),
    ]