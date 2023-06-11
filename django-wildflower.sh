bash
pip install django


bash
django-admin startproject wildflowercreek


bash
cd wildflowercreek
django-admin startapp store


python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


python
from django.shortcuts import render
from .models import Product

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


html
{% for product in products %}
    <div>
        <img src="{{ product.image.url }}" alt="{{ product.name }}">
        <h2>{{ product.name }}</h2>
        <p>{{ product.price }}</p>
    </div>
{% endfor %}


python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]


python
from django.urls import path, include

urlpatterns = [
    path('', include('store.urls')),
]


bash
python manage.py createsuperuser


python
from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)


bash
python manage.py runserver


python
from django.urls import path, include

urlpatterns = [
    path('', include('store.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]


