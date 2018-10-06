import time
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
start_time = time.time()

def get_all_names(lister):
    i = 0
    items = []
    a_items = []
    for element in lister:
        items.append(element.find('div', class_='ttl'))
        a_items.append(items[i].a.text)
        i += 1
    return a_items
def get_all_prices(lister):
    prices = []
    aprices = []
    for price in lister:
        aprices.append(price.find('div', class_='curr'))

    for price in aprices:
        text = str(int(price.text[:6].replace(' ', '')) * 0.95)
        prices.append(text)
    return prices
def get_all_texts(lister):
    atexts = []
    texts = []
    for element in lister:
        atexts.append(element.find('div', class_='cln-chars'))

    for element in atexts:
        texts.append(element.text)
    return texts#, 'характеристики', 'Наша Цена', 'фото' , row['about'], row['price']
def save(source, results):
    with open(source, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('title', 'price', 'images', 'about'))
        for row in results:
            writer.writerow((row['title'], row['price'], row['image'], row['about']))
        print('записанно ', len(results))
def main(path, url):

    html = urlopen(url + '?COUNT=100')
    
    bs = BeautifulSoup(html.read(), 'lxml')
    all = bs.find('div', class_='results-line')
    all_elements = all.find_all('div', class_='w')

    full_result = []
    names = get_all_names(all_elements)
    prices = get_all_prices(all_elements)
    texts = get_all_texts(all_elements)
    print(all_elements)
    #for i in range(0, len(names)):
     #   full_result.append({
      #      'name':names[i],
       #     'text': texts[i],
        #    'price': prices[i]
        #})
    #save(path, full_result)
    

if __name__ == '__main__':
    images = []
    names = []
    prices = []
    characteristics = []
    res = []
    html = urlopen('http://mikroklimat55.ru/?catalog=35')
    bs = BeautifulSoup(html.read(), 'lxml')
    all = bs.find('ul', id = 'catalog_cont')
    all_elements = all.find_all('li')
    
    for element in all_elements:
        names.append(element.find('a', id = 'title_catalog').text)
        img_div = element.find('div', id = 'preview_img')
        images.append(('http://mikroklimat55.ru/') + img_div.find('img').get('src'))

        txtPrice = element.find('span', id ='price_catalog').text[:7]
        txtPrice = txtPrice.replace(' ', '')
        price = str(int((int(txtPrice)*0.96)))
        prices.append(price)
        text = element.find('table')
        characteristics.append(text)
    for i in range(0, len(names)):
        res.append({
            'title': names[i],
            'image': images[i],
            'price': prices[i],
            'about': characteristics[i]
            })
    
    save('micro.csv', res)




