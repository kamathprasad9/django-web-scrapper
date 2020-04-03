from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request as req
from bs4 import BeautifulSoup as bs

def qry_flipkart(name):
    lst = name.split()
    qry_flipkart = 'https://www.flipkart.com/search?q='
    for l in lst:
        qry_flipkart = qry_flipkart + '+' + l
    return qry_flipkart

def filter(name):
    s = str(name).lower()
    # print(s)
    index = s.find('(')
    # print(s[0:index-1])
    return s[0:index - 1]

def qry_Amazon(name):
    lst = name.split()
    qry = 'https://www.amazon.in/s?k='
    for l in lst:
        qry = qry + '+' + l
    return qry

item = input("Enter name of product to search : ")

# #for flipkart
# flipkart_price,flipkart_link,flipkart_name,flipkart_rating,flipkart_img=[],[],[],[],[]
# print("Flipkart Query  "+qry_flipkart(item))
# data = req.urlopen(qry_flipkart(item)).read()
# soup = bs(data, 'lxml')
# temp = 0
# count = 0

# options = Options()
# driver = webdriver.Chrome(r'C:\Users\shubh\Desktop\chromedriver.exe', options=options)
# driver.get(qry_flipkart(item))
# driver.implicitly_wait(5)
# src=[]
# image = driver.find_elements_by_tag_name('img')
# for i in image:
#     src.append(i.get_attribute('src'))
# for a in src:
#     if 'q=70' in a:
#         if len(flipkart_img)<5:
#             flipkart_img.append(a)
# driver.close()

# def has_id_no_class(tag):
#     return tag.has_attr('data-id') and not tag.has_attr('class')
# for dataId in soup.findAll(has_id_no_class):
#     name = dataId.findChildren('div', {"class": "_3wU53n"})
#     if name == []:
#         name = dataId.findChildren('a', {"class": "_2cLu-l"})
#         temp += 1
#     else:
#         temp = 0  
#     name2 = name.copy()

#     rating = dataId.findChildren('div', {"class": "hGSR34"})
#     for r in rating:
#         if len(flipkart_rating)<5:
#             flipkart_rating.append(float(r.text))
#     flag = True
#     content = []
#     for item1 in name:
#         item1 = [content for content in item1.text.split('\n') if len(content) > 0]
#         item1 = ' '.join(item1)
#         content.append(item1)
#     for i in content:
#         if item.lower() in i.lower():
#             if len(flipkart_name)<5:
#                 flipkart_name.append(i)
#         else:
#             flag = False
    
#     price = dataId.findChildren('div', {"class": "_1vC4OE _2rQ-NK"})
#     if price == []:
#         price = dataId.findChildren('div', {"class": "_1vC4OE"})
#     content1 = []
#     for item2 in price:
#         item2 = [content1 for content1 in item2.text.split('\n') if len(content1) > 0]
#         item2 = ' '.join(item2)
#         content1.append(item2)
#     for i in content1:
#         if flag:
#             if len(flipkart_price)<5:
#                 flipkart_price.append(i)

#     links_with_text = []
#     if temp == 0:
#         for a in dataId.findChildren('a', {"class": "_31qSD5"}, href=True):
#             if a.text:
#                 links_with_text.append(a['href'])
#         for t in links_with_text:
#             if flag:
#                 if len(flipkart_link)<5:
#                     flipkart_link.append("https://www.flipkart.com"+t)
#     elif temp>0:
#         for i in name2:
#             links_with_text.append(i['href'])
#         for t in links_with_text:
#             if flag:
#                 if len(flipkart_link)<5:
#                     flipkart_link.append("https://www.flipkart.com"+t)

# print(flipkart_price,'\n',flipkart_link,'\n',flipkart_name,'\n',flipkart_rating,'\n',flipkart_img)
# print()
# print()

#for amazon
amazon_price,amazon_link,amazon_name,amazon_img,amazon_ratings=[],[],[],[],[]
print("Amazon Query  "+qry_Amazon(item))
data = req.urlopen(qry_Amazon(item)).read()
soup = bs(data, 'lxml')
count = 0
c=0
def has_data_asin(tag):
    return tag.has_attr('data-asin')

for dataId in soup.findAll(has_data_asin):
    name = dataId.findChildren('span', {"class": "a-size-medium a-color-base a-text-normal"})
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
        if item.lower() in i.lower():
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

    for t in links_with_text:
        if flag:
            #print("https://www.amazon.in"+t)
            if len(amazon_link)<5:
                amazon_link.append("https://www.amazon.in"+t)

print()
print()
print(amazon_price,'\n',amazon_link,'\n',amazon_name,'\n',amazon_img,'\n',amazon_ratings)