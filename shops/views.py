from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from .models import Shop
from django.contrib.gis.geos import Point
from django.shortcuts import render
from .forms import PostForm
import decimal
from django.shortcuts import redirect
from django.db.models import Q
from django.shortcuts import render, get_object_or_404



def shop_list(request):
    longitude = 80.0250203
    latitude = 13.5566102
    user_location = Point(longitude, latitude, srid=4326)
    query=""

    shops=[]
    if request.GET:
        query=request.GET['q']
        longitude=float(request.GET['long'])
        latitude=float(request.GET['lat'])
        user_location = Point(longitude, latitude, srid=4326)
    
        shops = Shop.objects.annotate(distance=Distance('location',
        user_location)
        ).order_by('distance')

        shops=shops.filter(Items_present__contains=[query]).distinct()
    else:
        shops = Shop.objects.annotate(distance=Distance('location',
        user_location)
        ).order_by('distance')

    
    return render(request, 'shops/index.html', {'shops': shops})


def shop_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.lattitude=float(form['lattitude'].value())
            shop.longitude=float(form['longitude'].value())
            shop.cover_image=form.cleaned_data['cover_image']
            shop.location=Point(shop.longitude, shop.lattitude)
            shop.save()
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'shops/shop_edit.html', {'form': form})

def shop_detail(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    return render(request, 'shops/shop_detail.html', {'shop': shop})
