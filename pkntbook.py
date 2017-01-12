
# coding: utf-8

# In[1]:

import pkntbasics
#import sqlite3
#import time
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
    bookname = soup.find_all('div', class_='dotd-title')[0].h2.string.strip()
    logger.debug('Bookname: ' + bookname)
    bookcover = 'http:'+soup.find_all('img', class_='imagecache-dotd_main_image')[0]['src']
    bookdescription = soup.find_all('div', class_='dotd-main-book-form')[0].previous_sibling.previous_sibling.text.strip()
    
    book = dict(name=bookname, description=bookdescription, coverimage=bookcover)
    return book

