import sys
sys.path.append("..")

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from shops import views
from django.conf import settings
from django.views.static import serve
from djgeojson.views import GeoJSONLayerView
from shops.models import Shop
from django.contrib.auth import views as auth_views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name = 'register'),
    path('login/', auth_views.LoginView.as_view(template_name = 'shops/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name = 'shops/logout.html'), name = 'logout'),
    path('', include('shops.urls')),

]





if settings.DEBUG:
    urlpatterns+=[
        url(r'^media/(?P<path>.*)$',serve,{
            'document_root':settings.MEDIA_ROOT
        }),
    ]