from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='scrape-home'),
    path('about/',views.about,name='scrape-about'),
]