import requests
import time
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Search
from requests.compat import quote_plus
from . import models

BASE_AMAZON_URL='https://www.amazon.in/s?k={}'

# Create your views here.
def home(request):
    return render(request,'scrape/home.html')

def about(request):
    return render(request,'scrape/about.html')

def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)
    final_url=BASE_AMAZON_URL.format(quote_plus(search))
    response=requests.get(final_url)
    data=response.text
    soup=BeautifulSoup(data,features='html.parser')
    name,amazon_ratings,amazon_name,amazon_img,amazon_price,amazon_link=[],[],[],[],[],[]
    for dataId in soup.findAll(has_data_asin):
        name=dataId.findChildren('span', {"class": "a-size-medium a-color-base a-text-normal"})
        if name==[]:
            name=dataId.findChildren('span', {"class": "a-size-base-plus a-color-base a-text-normal"})
        rating_ama = dataId.findChildren('span', {"class": "a-icon-alt"})
        for r2 in rating_ama:
            rt = r2.text
            x = rt.split(' ')
            if len(amazon_ratings)<5:
                amazon_ratings.append(float(x[0]))
            x.clear()
        flag = True
    
        content = []
        for item1 in name:
            item1 = [content for content in item1.text.split('\n') if len(content) > 0]
            item1 = ' '.join(item1)
            content.append(item1)
        for i in content:
            if search.lower() in i.lower():
                if len(amazon_name)<5:
                    amazon_name.append(i)
            else:
                flag = False
        price_flag = False
        
        image = dataId.findChildren('img', { "class" : "s-image" })
        #print(image[0]['src'])
        if len(amazon_img)<5:
            amazon_img.append(image[0]['src'])
            
        rating2 = dataId.findChildren('span', {"class": "a-size-medium a-color-base a-text-beside-button a-text-bold"})
        #print(rating2)
        price = dataId.findChildren('span', {"class": "a-color-price"})
        if(price == []):
            price = dataId.findChildren('span', {"class": "a-price-whole"})
            price_flag = True
        #print(price)
        content1 = []
        if price == [] and len(amazon_price)<5:
            amazon_price.append('NA')
        else:
            for item2 in price:
                item2 = [content1 for content1 in item2.text.split('\n') if len(content1) > 0]
                item2 = ' '.join(item2)
                content1.append(item2)
        for i in content1:
            if flag:
                if len(amazon_price)<5:
                    amazon_price.append(i)

        links_with_text = []
        for a in dataId.findChildren('a', {"class": "a-link-normal a-text-normal"}, href=True):
            if a.text:
                links_with_text.append(a['href'])
        if links_with_text==[]:
            for a in dataId.findChildren('a', {"class": "a-link-normal a-text-normal"}, href=True):
                if a.text:
                    links_with_text.append(a['href'])
        for t in links_with_text:
            if flag:
                #print("https://www.amazon.in"+t)
                if len(amazon_link)<5:
                    amazon_link.append("https://www.amazon.in"+t)
                

    print()
    print()
    print(amazon_price,'\n',amazon_link,'\n',amazon_name,'\n',amazon_img,'\n',amazon_ratings)
    stuff_for_frontend={
        'search':search
    }
    return render(request, 'scrape/new_search.html',stuff_for_frontend)

def has_data_asin(tag):
    return tag.has_attr('data-asin')