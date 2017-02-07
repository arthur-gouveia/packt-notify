
# coding: utf-8

# In[ ]:

import sqlite3
import pkntbasics


# In[ ]:

pkntbasics.config_loggers('DEBUG')
logger = pkntbasics.DBLOGGER


# In[ ]:

def sign_up(email_addr, id_last_book=None):
    import time
    global logger
    
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        if (isinstance(email_addr, str)):
            logger.debug('Inserting single value %s' %email_addr)
            cur.execute('''INSERT INTO tb_emails (nom_addr, dt_in, id_last_book)
                            VALUES (?, ?, ?)''', (email_addr, time.strftime('%Y-%m-%d'), id_last_book))
        elif (isinstance(email_addr, list)):
            now = time.strftime('%Y-%m-%d')
            to_insert = [(item, now, id_last_book) for item in email_addr]
            logger.debug('Inserting a list of %d values' %len(to_insert))
            cur.executemany('''INSERT INTO tb_emails (nom_addr, dt_in, id_last_book)
                               VALUES (?, ?, ?)''', to_insert)
        else:
            raise TypeError
        dbconn.commit()


def get_last_book():
    global logger
    
    logger.debug('Connecting to database to get last book')
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        logger.debug('Querying last book')
        data = cur.execute('Select rowid as mr, nom_book from tb_books order by rowid desc limit 1')
        lastbook = list(data)[0]
    return lastbook


def book_exists(bookname, quantity=2):
    global logger
    
    logger.debug('Connecting to database to check book existence')
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        logger.debug('Querying top %d books' %quantity)
        data = cur.execute('select * from tb_books limit ?', (quantity, ))
        bookslist = [book[1] for book in data]
        logger.debug('Got %d books' %len(bookslist))
    
    logger.debug('{} in {}'.format(bookname, bookslist))
    return bookname in bookslist


def insert_book(bookname):
    import time
    
    global logger
    
    logger.debug('Connecting to database to insert book')
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        logger.debug('Inserting data')
        cur.execute("""INSERT INTO tb_books (nom_book, dt_fetched)
                        VALUES (?, ?);""", (bookname, time.strftime('%Y-%m-%d %H:%M:%S')))
        dbconn.commit()
        
def get_recipients():
    global logger
    
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        logger.debug('Querying tb_emails')
        results = cur.execute('SELECT nom_addr FROM tb_emails')
        
    return results

