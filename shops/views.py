from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from .models import Shop
from django.contrib.gis.geos import Point
from django.shortcuts import render
from .forms import PostForm, ReviewForm
from django.shortcuts import redirect
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.gis.measure import Distance as dist
from django.contrib.auth.models import User
from django.core.mail import send_mail

import decimal


def shop_list(request):
    longitude = 80.0250203
    latitude = 13.5566102
    radius = 5
    user_location = Point(longitude, latitude, srid=4326)
    query=""

    shops=[]
    if request.GET:
        query=request.GET['q']
        longitude=float(request.GET['long'])
        latitude=float(request.GET['lat'])
        user_location = Point(longitude, latitude, srid=4326)

        while not shops:
            if radius>150:
                break
            radius+=5
            shops_within_radius=Shop.objects.filter(location__distance_lt=(user_location, dist(km=radius))) 

            if shops_within_radius:  
                shops = shops_within_radius.annotate(distance=Distance('location',
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
            shop.shop_owner=request.user.username
            shop.owner_email=request.user.email
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


def shop_edit(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None,instance=shop)
        if form.is_valid():
            shop = form.save()
            return redirect('shop_detail', pk=shop.pk)
    else:
        form = PostForm(instance=shop)
    return render(request, 'shops/shop_edit.html', {'form': form})


def shop_remove(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    shop.delete()
    return redirect('home')

def add_review_to_shop(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.shop = shop
            review.save()
            return redirect('shop_detail', pk=shop.pk)
    else:
        form = ReviewForm()
    return render(request, 'shops/add_review_to_shop.html', {'form': form}) 

def aboutUs(request):
    return render(request, 'shops/about.html',{})


def order(request):
    if request.method=="POST":
        customer_name=request.POST['customer-name']
        customer_email=request.POST.get('customer-email')
        customer_phone=request.POST.get('customer-phone')
        order_description=request.POST.get('order-description')
        owner_email=request.POST.get('owner-email')
        owner_name=request.POST.get('owner-name')
        message="Hello I am "+customer_name+ " my email is : "+customer_email+" and my contact number is : "+customer_phone+" and here is my Order description :  \n"+order_description
        send_mail(
            'Pre-Packaging Order',
            message,
            customer_email,
            [owner_email],
            fail_silently=False
        )

        return redirect('home')
        

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'{username}, Your account has been created!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'shops/register.html', {'form':form})

