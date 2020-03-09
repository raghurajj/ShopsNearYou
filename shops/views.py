from django.views import generic
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
from .models import Shop
from django.contrib.gis.geos import Point
from django.shortcuts import render
from .forms import PostForm
import decimal
from django.shortcuts import redirect

longitude = 80.0250203
latitude = 13.5566102

user_location = Point(longitude, latitude, srid=4326)




class Home(generic.ListView):
    model = Shop
    context_object_name = 'shops'
    queryset = Shop.objects.annotate(distance=Distance('location',
    user_location)
    ).order_by('distance')[0:10]
    template_name = 'shops/index.html'



def shop_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.lattitude=float(form['lattitude'].value())
            shop.longitude=float(form['longitude'].value())
            shop.cover_image=form.cleaned_data['cover_image']
            print(form.cleaned_data['cover_image'])
            shop.location=Point(shop.longitude, shop.lattitude)
            shop.save()
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'shops/shop_edit.html', {'form': form})