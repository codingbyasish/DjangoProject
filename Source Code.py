Source Code
viwes py

 from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Book
from .forms import BookForm
# Create your views here.
 
def index(request):
    book_list = Book.objects.all()
    context ={
        'book_list':book_list
    }
    return render(request,'myapp/index.html',context)
 
 
def detail(request,book_id):
    book = Book.objects.get(id=book_id)
    return render(request,'myapp/detail.html',{'book':book})
 
def add_book(request):
    if request.method == "POST":
        name = request.POST.get('name',)
        desc = request.POST.get('desc',)
        price = request.POST.get('price',)
        book_image = request.FILES['book_image']
 
        book = Book(name=name,desc=desc,price=price,book_image=book_image)
        book.save()
 
    return render(request,'myapp/add_book.html')
 
def update(request,id):
    book = Book.objects.get(id=id)
    form = BookForm(request.POST or None, request.FILES, instance=book)
    if form.is_valid():
        form.save()
        return redirect('/')
    return render(request,'myapp/edit.html',{'form':form,'book':book})
 
def delete(request,id):
    if request.method=="POST":
        book = Book.objects.get(id=id)
        book.delete()
        return redirect('/')
    return render(request,'myapp/delete.html')
    
  urls py

from django.contrib import admin
from django.urls import path
from myapp import views
 
app_name = 'myapp'
 
urlpatterns = [
   
    path('',views.index,name='index'),
    #book/2
    path('book/<int:book_id>/',views.detail,name='detail'),
    path('add/',views.add_book,name='add_book'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
]


models py

from django.db import models
 
# Create your models here.
 
class Book(models.Model):
 
    def __str__(self):
        return self.name
 
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    price = models.IntegerField()
    book_image = models.ImageField(default='default.jpg',upload_to='book_images/')
    




forms py

from django import forms
from .models import Book
 
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name','desc','book_image','price']


admin py

from django.contrib import admin
from .models import Book
# Register your models here.
 
admin.site.register(Book)
 




Templates

index html

{% extends 'myapp/base.html' %}
{% block body %}
 
<div class="container">
    <div class="row">
        {% for book in book_list %}
        <div class="col-md-3">
            <div class="card">
                <img src="{‌{book.book_image.url}}" class="card-img-top" alt="">
                <div class="card-body">
                    <h5 class="card-title">{‌{book.name}}</h5>
                    <p class="card-text">${‌{book.price}}</p>
                    <a class="btn btn-warning" href="{% url 'myapp:detail' book.id %}">View Details  </a> 
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
 
 
 
 
 
   
 
{% endblock %}
 
 

edit html

<form method="POST" enctype="multipart/form-data" >
    {% csrf_token %}
    {‌{form.as_p}}
    <input type="submit" name="" id="">
</form>


detail html

{% extends 'myapp/base.html' %}
 
{% block body %}
 
<div class="container">
    <div class="row">
        <div class="col-md-6">
                <img width="300" height="300" src="{‌{book.book_image.url}}">
 
        </div>
        <div class="col-md-6">
                <h2>{‌{book.name}} </h2>
 
                <h4>{‌{book.desc}}</h4>
                
                 <h6>{‌{book.price}}</h6>
                
                 <a class="btn btn-warning" href="{% url 'myapp:update' book.id %}">Update</a>
                 <a class="btn btn-danger" href="{% url 'myapp:delete' book.id %}">Delete</a>
                
        </div>
    </div>
</div>
 
 
 
{% endblock %}
 


delete html

<form method="POST">
    {% csrf_token %}
    Are you sure you want to delete this book?
    <input type="submit">
</form>


base html

{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="{% static 'myapp/style.css' %}">
 
    <title>Document</title>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <a class="navbar-brand" href="#">
          Online Book Store
        </a>
      </nav>
 
      {% block body %}
 
 
      {% endblock %}
 
</body>
</html>


add_book html

<form method="POST" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="text" name="name" id="name" placeholder="Enter name of the book" >
    <input type="text" name="desc" id="desc" placeholder="Enter book description">
    <input type="text" name="price" id="price" placeholder="Enter book Price">
    <input type="file" name="book_image" id="book_image">
    <input type="submit" name="" id="">
</form>
