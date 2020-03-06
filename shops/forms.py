from django import forms
from .models import Shop

class PostForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = ('name', 'lattitude','longitude','Items_present','cover_image')