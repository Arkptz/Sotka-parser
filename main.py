import requests
from bs4 import BeautifulSoup as bs
import re as regex
import logging_settings
import logging as log
from DB import SessionDb, FabricsDb

base_url = 'https://www.meb100.ru'
first_link = 'https://www.meb100.ru/ulyanovskaya-oblast/mebelnye-fabriki-opt'
resp = requests.get(first_link, timeout=30)
base_page = bs(resp.content, 'html.parser')
pagination = base_page.find('ul', attrs={'class':'pagination'})
count_pages = int(pagination.find_all('li')[-1].text)
log.info(f'Кол-во страниц -- {count_pages}')

local_links = [i[0]
               for i in SessionDb.query(FabricsDb.fabric_local_link).all()]


def delete_probels(text) -> str:
    try:
        return regex.findall(r'\w[^\t]*', text)[0]
    except:
        return ''


for page in range(1, count_pages+1):
    resp = requests.get(first_link, params={'page': page}, timeout=30)
    base_page = bs(resp.content, 'html.parser')
    fabrics = base_page.find_all(
        'div', attrs={'class': 'factory organization-preview'})
    fabrics_link = []
    for fabric in fabrics:
        name = fabric.find(
            'div', attrs={'class': 'col-sm-12 factory-title'}).text
        local_link = base_url + fabric.find('a').attrs['href']
        fabrics_link.append([name, local_link])
    log.info(f'Нашёл {len(fabrics_link)} фабрик на странице №{page}')
    for name, link in fabrics_link:
        if link in local_links:
            log.info('В бд уже есть эта фабрика')
            continue
        log.info(f'Get {link}...')
        resp = requests.get(link, timeout=30)
        fabric_page = bs(resp.content, 'html.parser')
        address = fabric_page.find('div', attrs={'id': 'content__address'}).text
        address = delete_probels(address)
        fabric_site = delete_probels(
            fabric_page.find('div', attrs={'class': 'content-line'}).text)
        fabric_site = fabric_site if '.' in fabric_site else 'нету'
        phones = ''
        div_phones = fabric_page.find(
            'div', attrs={'class': 'content-line phones-preview'})
        for i in div_phones.find_all('span'):
            phones += delete_probels(i.text) + ',   '
        segments_elem = fabric_page.find(
            'div', attrs={'class': 'col-xs-8 col-md-6 shot-description'})
        segment_v1 = ''
        if segments_elem:
            segment_v1 = delete_probels(segments_elem.text)
        nav = fabric_page.find('ul', attrs={'class': 'nav nav-products'})
        segments_v2 = ''
        for elem in nav.find_all('li'):
            text = elem.find('span', attrs={'class': 'type-name'}).text
            segments_v2 += delete_probels(text) + ',   '
        check_sst = False
        full_segments = segment_v1.lower() + segments_v2.lower()
        if ('стол' in full_segments) or ('стул' in full_segments) or ('табурет' in full_segments):
            check_sst = True
        Fabric = FabricsDb(name=name, address=address, fabric_site=fabric_site, phones=phones,
                           segments_v1=segment_v1, segments_v2=segments_v2, fabric_local_link=link, stol_styl_tabyret=check_sst)
        SessionDb.add(Fabric)
        SessionDb.commit()
        SessionDb.flush()
        log.info('Спарсил фабрику...\n'
                 f'Name - {name}\n'
                 f'Address - {address}\n'
                 f'Phones - {phones}\n'
                 f'Site - {fabric_site}\n'
                 f'Segments_v1 - {segment_v1}\n'
                 f'Segments_v2 - {segments_v2}\n'
                 f'Check_sst - {check_sst}\n\n\n')
