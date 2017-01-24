import time
import logging
from collections import namedtuple
import urllib.request
import os

import telepot
from bs4 import BeautifulSoup



logger = logging.getLogger('pknt-bot')
handler = logging.StreamHandler()
formatter = logging.Formatter(
        '%(asctime)s %(name)-15s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel('WARNING')


def notify_free(bot, chatid, book):   
    global logger
    
    now = time.strftime('%d/%m/%Y')
    link = 'https://www.packtpub.com/packt/offers/free-learning'
    caption = '({0}) {1.name}. Download at {2}'.format(now, book, link)
    image = book.cover
    logger.debug('Caption is ' + caption)
    logger.debug('Image URL: ' + image)
    msg = bot.sendMessage(chatid,
                          'The FREE book of today ({0}) is\n*{1.name}*\n\n{1.textdescription}'.format(now, book),
                          parse_mode='Markdown')
    logger.debug('Sent book description: {!s}'.format(msg))
    msg = bot.sendPhoto(chatid, image, caption=caption)
    logger.debug('Sent book cover image: {!s}'.format(msg))


def notify_deals(bot, chatid, books):   
    global logger
    
    now = time.strftime('%d/%m/%Y')
    link = 'https://www.packtpub.com/books/deal-of-the-day'

    msg = bot.sendMessage(chatid,
                          '*Deals of the day {}*\nBuy at {}'.format(now, link),
                          parse_mode='Markdown',
                          disable_web_page_preview=True)
    logger.debug('Initial deals of the day message: {!s}'.format(msg))
    for i in range(4):
        caption = 'Deal #{0}: {1.name}.\nNormal price {1.rrp}\nToday price {1.price}'.format(i+1, books[i])
        logger.debug('Caption {} is {}'.format(i+1, caption))
        logger.debug('Image {} URL: {}'.format(i+1, books[i].cover))
        msg = bot.sendPhoto(chatid, books[i].cover, caption=caption)
        logger.debug('Sent book cover: {!s}'.format(msg))


def get_page(url):
    global logger
       
    logger.debug('Reading URL '+url)
    data = urllib.request.urlopen(url).read()
    logger.debug('Read %d data' %len(data))
    logger.debug('Parsing data')
    soup = BeautifulSoup(data, 'html.parser')
    
    return soup


def get_free_book(url):
    global logger
    
    soup = get_page(url)
    
    logger.debug('Getting bookname')
    bookname = soup.find_all('div', class_='dotd-title')[0].text.strip()
    logger.debug('Bookname: ' + bookname)
    bookcover = 'https:'+soup.find_all('img', class_='imagecache-dotd_main_image')[0]['src'].replace(' ', '%20')
    bookdescription = soup.find_all('div', class_='dotd-main-book-form')[0].previous_sibling.previous_sibling
    textdescription = bookdescription.text.strip()
    bookdescription = str(bookdescription)
    
    Book = namedtuple('FreeBook', ['cover', 'name', 'htmldescription', 'textdescription'])
    
    book = Book(bookcover, bookname, bookdescription, textdescription)
    return book


def get_deal_books(url):
    global logger
    
    soup = get_page(url)
    Book = namedtuple('DealOfTheDayBook', ['cover', 'name', 'description', 'price', 'rrp'])
    FourBooks = namedtuple('DealsOfTheDay', 'main second third fourth')
    
    # Main deal of the day
    bookname = soup.find_all('div', class_="dotd-main-book-title")[0].text.strip()
    bookdescription = soup.find_all('div', class_="dotd-main-book-text")[0].text.strip()
    bookcover = 'https:'+soup.find_all('img', class_='imagecache-dotd_main_image')[0]['src'].replace(' ', '%20')
    bookprice = soup.find_all('div', class_='book-top-pricing-main-ebook-price')[0].text.strip()
    bookrrprice = soup.find_all('div', class_='dotd-rrp-price float-left')[0].text.strip()[4:]
    
    
    secondary_books = soup.find_all('div', class_='book-block')
    keys = ['second', 'third', 'fourth']
    
    minordeals = []
    for secondary_book in secondary_books:
        if 'last' in secondary_book['class']:
            break
        sbname = secondary_book.find('div', class_="book-block-title").text.strip()
        sbcover = 'https:'+secondary_book.find('img', class_='bookimage dotd')['src'].replace(' ', '%20')
        sbprice = secondary_book.find('div', class_='book-block-price').text.strip()
        sbrrp = secondary_book.find('div', class_='book-block-rrp').text.strip()[5:]
        minordeals.append(Book(sbcover, sbname, None, sbprice, sbrrp))
    
    booksdict = {key: book for key, book in zip(keys, minordeals)}
    
    booksdict['main'] = Book(bookcover, bookname, bookdescription, bookprice, bookrrprice)
    
    books = FourBooks(**booksdict)
    
    return books

def main():
    botkey = os.environ['BOTKEY']
    bot = telepot.Bot(botkey.replace("'", ""))
    chatid = '@packtpubnotify'
    freebook = get_free_book('https://www.packtpub.com/packt/offers/free-learning')
    deal_books = get_deal_books('https://www.packtpub.com/books/deal-of-the-day')
    notify_free(bot, chatid, freebook)
    notify_deals(bot, chatid, deal_books)


if __name__ == '__main__':
    main()
