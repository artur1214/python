import time
import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
start_time = time.time()
def save(source, results):
    with open(source, 'w', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('title', 'price', 'images', 'about', 'mainDesc'))
        for row in results:
            writer.writerow((row['title'], row['price'], row['image'], row['about'], row['main_desc']))
        print('записанно ', len(results))



def parceMainText(pages):
    texts = []
    for page in pages:
        html = urlopen('http://mikroklimat55.ru/' + page)
        bs = BeautifulSoup(html.read(), 'lxml')
        text = bs.find('div', id ='brief_desc')
        texts.append(text)
    return texts

def get_texts(url):
    pass
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'lxml')
    all = bs.find('ul', id = 'catalog_cont')
    all_elements = all.find_all('li')
    lincs =[]
    for product in all_elements:
        page = product.find('a', id = 'title_catalog')
        lincs.append(page.get('href'))
    print(lincs)
    opis = parceMainText(lincs)
    return opis


if __name__ == '__main__':
    images = []
    names = []
    prices = []
    characteristics = []
    res = []
    main_texts =[]
    url = 'http://mikroklimat55.ru/?catalog=21'
    html = urlopen(url)
    bs = BeautifulSoup(html.read(), 'lxml')
    all = bs.find('ul', id = 'catalog_cont')
    all_elements = all.find_all('li')
    main_texts =  get_texts(url)
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
            'about': characteristics[i],
            'main_desc': main_texts[i]
            })
    
    save('micro.csv', res)



    # MDV, Daicin, kentatsu, midea, ballu, lessar, tosot, samsung, zanussi, electrolux, LG, haier, 