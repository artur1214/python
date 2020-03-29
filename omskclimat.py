from bs4 import BeautifulSoup
import requests
import csv
import re
from lxml import html
MAIN_URL = 'http://xn--80apfafdek2aq.xn--p1ai'
URL = 'http://xn--80apfafdek2aq.xn--p1ai/mobilnye-konditsionery'
p = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
def save(data, path):
    with open(path, "w", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['title', 'price', 'photoes', 'description', 'charakteristics'])
        for line in data:
            writer.writerow([line['title'], line['price'], line['photoes'], line['description'], line['characteristics']])
def parse_main_data(links):
    to_save = []
    for i in links:
        page = requests.get(MAIN_URL + i)
        parser = BeautifulSoup(page.text)
        cur_page = {}

        main_body = parser.find('div', id = 'comjshop')
        price = parser.find('h2', class_ = 'prod_price')
        price = price.text
        price = price.split('руб')

        price = ''.join(i for i in price[0] if i.isdigit())


        title = main_body.find('h1', class_ = 'uk-h2')                                       #Название
        main_body2 = main_body.find('div', class_ = 'uk-grid')
        photo = main_body2.find('div', id = 'list_product_image_middle')
        photoes = photo.find_all('a', class_ = 'lightbox')
        photoes1 = []                                                                        #Фотографии
        for i in photoes:
            photoes1.append(i.get('href'))
        description = main_body.find('ul', id = "tab-content").find('li')        #Описание
        #desc = description

        caracteristics = main_body.find('ul', class_ = 'uk-panel').find('table')#характеристики

        to_save.append({'title': title, 'price': price, 'photoes': photoes1, 'description': description, 'characteristics': caracteristics})
    return to_save

def main():

    site = requests.get(URL)
    res = BeautifulSoup(site.text)


    list = res.find('div', class_ = 'jshop list_product')
    products = list.find_all('div', class_ = 'name')
    l = []
    links = []
    for product in products:
        links.append(product.find('a').get('href'))

    res = parse_main_data(links)
    save(res, 'test.csv')
    for i in res:
        print(i)

if __name__ == '__main__':
    main()