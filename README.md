# Web Scraping From Sahibinden
This project includes a web scraping script that extracting data from sahibinden website. Sahibinden is a website which is used for
renting or purchases of assets like house and cars. Its very popular among the turkish people. Therefore, to analyze the market of houses in Turkey,
datas from sahibinden have a crucial role.

For the above reason, a scraper will help the data collection stage. My scraper project includes:

**•requirements.txt** : *includes packages that used in the project*\
**•runtime.txt** : *includes the version of python*\
**•sahibinden.py** : *main script of my project*\
**•results.csv** : *40-50 row datas which are extracted from sahibinden*\
**•proxy_.py** : *that includes a proxy scraper from /free-proxy-list.net/* **(Optional)**

**Note:** *sahibinden.py script sends too many get requests to sahibinden website. Instead of time sleeps, using only this script will 
eventually causes **HTTP 429 Too Many Requests** response. To avoid that response, request sender machine needs to change its IP.*
<br>
<br><br><br>
## Columns of the data
**baslik** : *title*\
**oda_sayisi** : *number of rooms*\
**tarih** : *uploaded date*\
**m2brut** : *gross square meter*\
**m2net** : *net square meter*\
**bulundugu_kat** : *floor of apartment*\
**kat_sayisi** : *total floor of building*\
**banyo_sayisi** : *total number of bathroom*\
**isitma** : *heating service of house*\
**balkon** : *having balcony*\
**esyali** : *having furnitures*\
**site_icinde** : *residence*\
**bina_yasi** : *age of building*\
**ilce / mahalle** : *location of house*\
**fiyat** : *renting price of house*\
**url** : *announcment url*\
