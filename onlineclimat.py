import re
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup


def save(source, results):
    with open(source, 'w', encoding='UTF-8') as csvfile:
        results = results[::-1]
        writer = csv.writer(csvfile)
        writer.writerow(('title', 'price', 'images', 'about', 'mainDesc'))
        for row in results:
            writer.writerow((row['title'], row['price'], row['image'], row['about'], row['main_desc']))
        print('записанно ', len(results))


def get_texts(url):
    res = []
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'lxml')
    all = bs.find('div', id='content_right')
    info1 = all.find('div', class_='product_info')
    price = all.find('div', class_='price')
    #print
    print(price)
    price = price.find('span').text

    price = price.replace(' ', '')
    price = int(price)-200
    price = str(price)
    imgElement = all.find('div', class_='image')
    img = imgElement.find('a').get('href')

    opis = all.find('div', id='opisanie')

    desc = opis.find('ul', class_='description_tab')
    d = str(desc)
    d = re.sub('/files/uploads/', 'http://onlineclimate.ru/files/uploads/', d)
    charect = all.find('div', id='charakteristiki')
    #print(d)
    characteristics = charect.find('ul', class_='description_tab')
    return price, img, d, characteristics


images = []
names = []
prices = []
characteristics = []
mainRes = []
res = []
main_texts = []
all_pg = []
res = []
url = 'https://onlineclimate.ru/catalog/nastennye-konditsionery/mdv?page=all'
html = urlopen(url)
bs = BeautifulSoup(html.read(), 'lxml')
all = bs.find('ul', class_='tiny_products')

tinyProd = all.find_all('li', class_="product")
prd = []
for prod in tinyProd:
    prd.append(prod.find('div', class_='product_info'))

for product in range(len(prd)):
    prod_name = prd[product].find('a', class_='product-url')
    names.append(prod_name.text)
    all_pg.append(prod_name.get('href'))
for pg in all_pg:
    try:
        price, img, desc, characteristics = get_texts('http://onlineclimate.ru/' + pg)
    except AttributeError:
        print('нет в наличии')
        continue

    res.append({
        'price': price,
        'img': img,
        'desc': desc,
        'characteristics': characteristics
    })

for i in range(len(res)):
    #print(i)
    el = res[i]
    #print(el['price'])
    mainRes.append({
        'title': names[i],
        'price': el['price'],
        'image': el['img'],
        'about': el['characteristics'],
        'main_desc': el['desc']
    })

save('online.csv', mainRes)

# writer.writerow((row['title'], row['price'], row['image'], row['about'], row['main_desc']))
