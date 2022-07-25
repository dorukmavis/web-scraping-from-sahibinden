from time import sleep
import requests
from bs4 import BeautifulSoup
#Response header settings

header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Upgrade-Insecure-Requests': '1',
} 


def get_proxies():
    proxy_list = []
    r = requests.get('https://free-proxy-list.net/',headers=header)
    print(f'https://free-proxy-list.net/ ---- {r.status_code}')
    soup = BeautifulSoup(r.text,'html5lib')
    all_proxies = soup.find('table',{'class':'table table-striped table-bordered'}).find_all('tr',class_=None)
    all_proxies.pop(0)
    all_proxies = all_proxies[:60]
    for proxy in all_proxies:
        ip = proxy.find_all('td',class_=None)[0].text.strip()
        port = proxy.find_all('td',class_=None)[1].text.strip()
        proxy_list.append(f'{ip}:{port}')
    return proxy_list
    
    

def get_responsive_proxy(url):
    proxies = get_proxies()
    while True:
        
        for proxy in proxies:
            try:
                response = requests.get(url,headers=header,proxies={'http':proxy,'https':proxy},timeout=3)
                if response.status_code==200:
                    print(f'{proxy} has successfully connected to {url}')
                    return response
            except:
                print(f'failed--{proxy}')
        
        sleep(0.5)
        proxies = get_proxies()
            

rp = get_responsive_proxy('https://sahibinden.com/kiralik-daire/istanbul')
soup = BeautifulSoup(rp.text,'html5lib')

print(soup)
