import requests
from django.shortcuts import render
from .models import Post
from bs4 import BeautifulSoup

# Create your views here.
def home(request):
    return render(request,'scrape/home.html')

def about(request):
    return render(request,'scrape/about.html')

def new_search(request):
    search=request.POST.get('search')
    print(search)
    stuff_for_frontend={
        'search':search
    }
    return render(request, 'scrape/new_search.html',stuff_for_frontend)