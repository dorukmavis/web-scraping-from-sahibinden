import requests
from bs4 import BeautifulSoup
import csv
from time import sleep
import re
import os 

PATH = os.path.join(os.path.dirname(__file__))

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
}


def get_date(date):

    DATES = {
        'Ocak':'1','Şubat':'2','Mart':'3','Nisan':'4',
        'Mayıs':'5','Haziran':'6','Temmuz':'7','Ağustos':'8',
        'Eylül':'9','Ekim':'10','Kasım':'11','Aralık':'12'
    }

    day = date.split(' ')[-3]
    month = DATES[date.split(' ')[-2]]
    year = date.split(' ')[-1]
    return f'{year}-{month}-{day}'

def write_csv(data):
    title = data['baslik']
    print(f'Writing {title} - data to csv...')
    sleep(2)
    with open('results.csv','a',newline='',encoding='UTF-8') as file:
        fields = ['baslik','oda_sayisi','tarih','m2brut','m2net','bulundugu_kat','kat_sayisi','banyo_sayisi','isitma','balkon','esyali','site_icinde','bina_yasi','ilce','mahalle','fiyat','url']
        writer = csv.DictWriter(file,fieldnames=fields)
        writer.writerow(data)
        print('Data has successfully appended.')


def get_urls(gc_url):

    print('Extracting content urls..')
    sleep(2)
    response = requests.get(gc_url,headers=header)

    while response.status_code==429:
        response = requests.get(gc_url,headers=header)
        sleep(120)
        print(f'HTTP {response.status_code}')
    
    print(f'HTTP {response.status_code}')
    sleep(2)

    soup = BeautifulSoup(response.text,'html5lib')

    urls = soup.find_all('a',{'class':'classifiedTitle'})
    urls = [url['href'] for url in urls]

    print(f'{len(urls)} urls successfully extracted.')
    sleep(2)
    return urls


def get_content(cont_url):

    sleep(2)
    cont_url = 'https://sahibinden.com'+cont_url
    print(f'Preparing for scrapping from {cont_url}... ')
    response = requests.get(cont_url,headers=header)

    while response.status_code==429:
        response = requests.get(cont_url,headers=header)
        sleep(120)
        print(f'HTTP {response.status_code}')
    
    print(f'HTTP {response.status_code}')
    sleep(2)

    soup = BeautifulSoup(response.text,'html5lib')
    
    print('Scrapping details...')
    sleep(2)
    details = soup.find('ul',{'class':'classifiedInfoList'})

    
    baslik = soup.find('div',{'class':'classifiedDetailTitle'}).h1.text
    fiyat = soup.find('div',{'class':'classifiedInfo'}).h3.text.split('\n')[1][:-2].strip()
    tarih = get_date(details.find_all('span')[1].text.strip())
    m2brut = details.find_all('span')[3].text.strip()
    m2net = details.find_all('span')[4].text.strip()
    oda_sayisi = details.find_all('span')[5].text.strip()

    cf_info = soup.find('div',{'class':'classifiedInfo'})
    lokasyon = cf_info.find_all('a',{'data-click-category':'İlan Detay Events'})
    ilce = lokasyon[1].text.strip()
    mahalle = lokasyon[2].text.strip()

    try:
        bina_yasi = int(re.search(r'\d+', details.find_all('span')[6].text).group())
    except:
        bina_yasi=''

    try:
        bulundugu_kat = int(re.search(r'\d+', details.find_all('span')[7].text).group())
    except:
        bulundugu_kat = ''

    try:
        kat_sayisi = int(re.search(r'\d+', details.find_all('span')[8].text).group())
    except:
        kat_sayisi=''
 
    try:
        banyo_sayisi = int(re.search(r'\d+', details.find_all('span')[10].text).group())
    except:
        banyo_sayisi=''

    isitma = details.find_all('span')[9].text.strip()
    balkon = details.find_all('span')[11].text.strip()
    esyali = details.find_all('span')[12].text.strip()
    site_icinde = details.find_all('span')[14].text.strip()
    url = cont_url

    
    
    data = {
        'baslik':baslik,'oda_sayisi':oda_sayisi,'tarih':tarih,'m2brut':m2brut,
        'm2net':m2net,'kat_sayisi':kat_sayisi,'bulundugu_kat':bulundugu_kat,'banyo_sayisi':banyo_sayisi,
        'isitma':isitma,'balkon':balkon,'esyali':esyali,'site_icinde':site_icinde,'bina_yasi':bina_yasi,
        'ilce':ilce,'mahalle':mahalle,'fiyat':fiyat,'url':url,
    }
    
    write_csv(data)
    sleep(2)
    

def get_next_page_url(gnp_url):

    print('getting next page url....')
    sleep(2)
    response = requests.get(gnp_url,headers=header)

    while response.status_code==429:
        response = requests.get(gnp_url,headers=header)
        sleep(120)
        print(f'HTTP {response.status_code}')

    print(f'HTTP {response.status_code}')

    soup = BeautifulSoup(response.text,'html5lib')
    nav = soup.find('ul',{'class':'pageNaviButtons'})
    next_b = nav.find('a',{'class':'prevNextBut','title':'Sonraki'})
    href = next_b['href']
    href = f'https://sahibinden.com{href}'
    sleep(2)

    print(f'next url : {href}')
    return href


def get_content_from_urls(g_url):
    urls = get_urls(g_url)
    for url in urls:
        get_content(url)

    new_url = get_next_page_url(g_url)
    return new_url

def main():

    url ='https://sahibinden.com/kiralik-daire/istanbul?pagingOffset=200&pagingSize=50'

    while True:
        nxt_url = get_content_from_urls(url)
        url = nxt_url
        print('Current operating url : '+url)  


if __name__ == '__main__':
    main()