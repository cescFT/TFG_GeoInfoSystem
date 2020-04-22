from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from GeoInfoSystem.models import *

class ImageUploadForm(forms.Form):
    image=forms.ImageField()

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"] # surt en l'ordre en que li poso aqui

class crearpuntInteres(forms.Form):
    latitud = forms.FloatField()
    longitud = forms.FloatField()
    idMapa = forms.IntegerField()
    tipus = forms.CharField(max_length=30)
    actiu = forms.BooleanField()
    superficie = forms.FloatField()
    localitat = forms.CharField(max_length=40)
    pais = forms.CharField(max_length=40)

    class Meta:
        model = puntInteres
        fields = ["latitud","longitud","idMapa","tipus", "actiu", "superficie", "localitat", "pais"]