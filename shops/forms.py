from django import forms
from .models import Shop, Review
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):

    class Meta:
        model = Shop
        fields = ('name', 'lattitude','longitude','Items_present','cover_image','image_with_Aadhar')

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ('customer', 'text',) 

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()
	contact = forms.CharField()

	class Meta:
		model = User
		fields = ['username', 'email', 'contact', 'password1', 'password2']

