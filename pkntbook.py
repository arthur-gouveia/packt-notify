
# coding: utf-8

# In[1]:

import pkntbasics
import urllib.request
from bs4 import BeautifulSoup


pkntbasics.config_loggers('WARNING')
logger = pkntbasics.BOOKLOGGER


# In[2]:

def get_page(url):
    global logger
    
    logger.debug('Reading URL '+url)
    data = urllib.request.urlopen(url).read()
    logger.debug('Read %d data' %len(data))
    logger.debug('Parsing data')
    soup = BeautifulSoup(data, 'html.parser')
    
    return soup

def get_book(url):
    global logger
    
    soup = get_page(url)
    
    logger.debug('Getting bookname')
    bookname = soup.find('div', class_='dotd-title').get_text().strip()
    logger.debug('Bookname: ' + bookname)
    bookcover = 'http:'+soup.find('img', class_='imagecache-dotd_main_image')['src']
    bookdescription = str(soup.find('div', class_='dotd-main-book-form').previous_sibling.previous_sibling)
    
    book = dict(name=bookname, description=bookdescription, coverimage=bookcover)
    return book

