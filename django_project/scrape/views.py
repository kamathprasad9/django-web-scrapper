import requests
import time
from bs4 import BeautifulSoup
from django.shortcuts import render
from .models import Search
from requests.compat import quote_plus
from . import models
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

BASE_AMAZON_URL='https://www.amazon.in/s?k={}'
BASE_FLIPKART_URL='https://www.flipkart.com/search?q={}'
BASE_SNAPDEAL_URL='https://www.snapdeal.com/search?keyword={}'

# Create your views here.
def home(request):
    stuff_for_frontend={
        'title': "Home",
    }
    return render(request,'scrape/home.html',stuff_for_frontend)

def new_search(request):
    search=request.POST.get('search')
    models.Search.objects.create(search=search)

    #AMAZON STUFF HERE
    final_amazon_url=BASE_AMAZON_URL.format(quote_plus(search))
    response=requests.get(final_amazon_url)
    data=response.content
    soup=BeautifulSoup(data,features='html.parser')
    name,amazon_ratings,amazon_name,amazon_img,amazon_price,amazon_link=[],[],[],[],[],[]
    amazon_postings=[]
    #count_ratings=0
    for dataId in soup.findAll(has_data_asin):
        name=dataId.findChildren('span', {"class": "a-size-medium a-color-base a-text-normal"})
        if name==[]:
            name=dataId.findChildren('span', {"class": "a-size-base-plus a-color-base a-text-normal"})
        rating_ama = dataId.findChildren('span', {"class": "a-icon-alt"})
        for r2 in rating_ama:
            rt = r2.text
            x = rt.split(' ')
            print(r2)
            if (len(amazon_ratings))<3:
                
                print(amazon_ratings)
                if r2==[]:
                    amazon_ratings.append(-1)
                else:
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
                if len(amazon_name)<3:
                    amazon_name.append(i)
            else:
                flag = False
        price_flag = False
        
        image = dataId.findChildren('img', { "class" : "s-image" })
        #print(image[0]['src'])
        if len(amazon_img)<3:
            amazon_img.append(image[0]['src'])
            
        rating2 = dataId.findChildren('span', {"class": "a-size-medium a-color-base a-text-beside-button a-text-bold"})
        #print(rating2)
        price = dataId.findChildren('span', {"class": "a-color-price"})
        if(price == []):
            price = dataId.findChildren('span', {"class": "a-price-whole"})
            price_flag = True
        #print(price)
        content1 = []
        if price == [] and len(amazon_price)<3:
            amazon_price.append('NA')
        else:
            for item2 in price:
                item2 = [content1 for content1 in item2.text.split('\n') if len(content1) > 0]
                item2 = ' '.join(item2)
                content1.append(item2)
        for i in content1:
            if flag:
                if len(amazon_price)<3:
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
                if len(amazon_link)<3:
                    amazon_link.append("https://www.amazon.in"+t)
        
        if len(amazon_link)==3:
            break

    m=len(amazon_name)
    n=len(amazon_ratings)
    if n<m:
        while n!=m:
            amazon_ratings.append(-1)
            n+=1
    if len(amazon_name)>0:  
        #print(amazon_name,len(amazon_price),len(amazon_name),len(amazon_ratings)) 
        for i in range(len(amazon_name)):
            print(i)
            amazon_postings.append((amazon_name[i],amazon_link[i],amazon_price[i],amazon_img[i],amazon_ratings[i]))
    
    print("AMAZON:\n",amazon_img,'\n',amazon_price,'\n',amazon_name,'\n',amazon_link,'\n',amazon_ratings)
    

    # FLIPKART STUFF HERE
    
    final_flipkart_url=BASE_FLIPKART_URL.format(quote_plus(search))
    response=requests.get(final_flipkart_url)
    data=response.content
    soup=BeautifulSoup(data,features='html.parser')
    flipkart_price,flipkart_link,flipkart_name,flipkart_rating,flipkart_img=[],[],[],[],[]
    temp,count=0,0

    options = Options()
    driver = webdriver.Chrome(r'D:\Downloads\chromedriver.exe', options=options)
    driver.get(final_flipkart_url)
    driver.implicitly_wait(2)
    src=[]
    image = driver.find_elements_by_tag_name('img')
    for i in image:
        src.append(i.get_attribute('src'))
    for a in src:
        if 'q=70' in a:
            if len(flipkart_img)<3:
                flipkart_img.append(a)
    driver.close()

    for dataId in soup.findAll(has_id_no_class):
        name = dataId.findChildren('div', {"class": "_3wU53n"})
        if name == []:
            name = dataId.findChildren('a', {"class": "_2cLu-l"})
            temp += 1
        else:
            temp = 0  
        name2 = name.copy()
        image = dataId.findChildren('img')
        #print(image)
        rating = dataId.findChildren('div', {"class": "hGSR34"})
        for r in rating:
            if len(flipkart_rating)<3:
                flipkart_rating.append(float(r.text))
        flag = True
        content = []
        for item1 in name:
            item1 = [content for content in item1.text.split('\n') if len(content) > 0]
            item1 = ' '.join(item1)
            content.append(item1)
        for i in content:
            if search.lower() in i.lower():
                if len(flipkart_name)<3:
                    flipkart_name.append(i)
            else:
                flag = False
        
        price = dataId.findChildren('div', {"class": "_1vC4OE _2rQ-NK"})
        if price == []:
            price = dataId.findChildren('div', {"class": "_1vC4OE"})
        content1 = []
        for item2 in price:
            item2 = [content1 for content1 in item2.text.split('\n') if len(content1) > 0]
            item2 = ' '.join(item2)
            content1.append(item2)
        for i in content1:
            if flag:
                if len(flipkart_price)<3:
                    flipkart_price.append(i)

        links_with_text = []
        if temp == 0:
            for a in dataId.findChildren('a', {"class": "_31qSD5"}, href=True):
                if a.text:
                    links_with_text.append(a['href'])
            for t in links_with_text:
                if flag:
                    if len(flipkart_link)<3:
                        flipkart_link.append("https://www.flipkart.com"+t)
        elif temp>0:
            for i in name2:
                links_with_text.append(i['href'])
            for t in links_with_text:
                if flag:
                    if len(flipkart_link)<3:
                        flipkart_link.append("https://www.flipkart.com"+t)

    print("FLIPKART\n",flipkart_price,'\n',flipkart_link,'\n',flipkart_name,'\n',flipkart_rating,'\n',flipkart_img)
    flipkart_postings=[]
    if len(flipkart_name)>0:
        for i in range(len(flipkart_name)):
            # print(i)
            flipkart_postings.append((flipkart_name[i],flipkart_link[i],flipkart_price[i],flipkart_img[i],flipkart_rating[i]))







    #SNAPDEAL STUFF HERE
    final_SD_url=BASE_SNAPDEAL_URL.format(quote_plus(search))
    response=requests.get(final_SD_url)
    data=response.content
    soup=BeautifulSoup(data,features='html.parser')
    SD_price,SD_link,SD_name,SD_rating,SD_img=[],[],[],[],[]
    image = soup.findChildren('img', { "class" : "product-image" })
    price = soup.findChildren('span', { "class" : "lfloat product-price" })
    name = soup.findChildren('p', { "class" : "product-title" })
    link = soup.findChildren('a', { "class" : "dp-widget-link noUdLine" }, href = True)
    #print(price)
    for i in image:
        if len(SD_img)<3:
            if i==[]:
                SD_img.append('NA')
            else:
                SD_img.append(i['src'])
    for j in price:
        if len(SD_price)<3:
            if j==[]:
                SD_price.append('Price Unavailable')
            else:
                SD_price.append(j.text)
    for n in name:
        if len(SD_name)<3:
            if n==[]:
                SD_name.append('Name not available')
            else:
                SD_name.append(n.text)
    for l in link:
        if len(SD_link)<3:
            if l==[]:
                SD_link.append('#')
            else:
                SD_link.append(l['href'])
    # print()
    # print()
    print("SD:\n",SD_img,'\n',SD_price,'\n',SD_name,'\n',SD_link)
    SD_postings=[]
    if len(SD_name)>0:
        for i in range(len(SD_name)):
            # print(i)
            SD_postings.append((SD_name[i],SD_link[i],SD_price[i],SD_img[i]))
    

    stuff_for_frontend={
        'title': search.capitalize(),
        'search':search,
        'amazon_postings':amazon_postings,
        'flipkart_postings': flipkart_postings,
        'SD_postings': SD_postings,
    }
    return render(request, 'scrape/new_search.html',stuff_for_frontend)



def has_data_asin(tag): #for amazon
    return tag.has_attr('data-asin')

def has_id_no_class(tag): #for flipkart
    return tag.has_attr('data-id') and not tag.has_attr('class')