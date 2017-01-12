
# coding: utf-8

# In[5]:

import sqlite3


# In[3]:

def sign_up(email_addr, id_last_book=None):
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        cur.execute('''INSERT INTO tb_emails (nom_addr, dt_in, id_last_book)
                        VALUES (?, ?, ?)''', (email_addr, time.strftime('%Y-%m-%d %H:%M:%S'), id_last_book))

        dbconn.commit()


def get_last_book():
    logger.debug('Connecting to database to get last book')
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        logger.debug('Querying last book')
        data = cur.execute('Select rowid as mr, nom_book from tb_books order by rowid desc limit 1')
        lastbook = list(data)[0]
    return lastbook


def book_exists(bookname, quantity=2):
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
    global logger
    
    logger.debug('Connecting to database to insert book')
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        logger.debug('Inserting data')
        cur.execute("""INSERT INTO tb_books (nom_book, dt_fetched)
                        VALUES (?, ?);""", (bookname, time.strftime('%Y-%m-%d %H:%M:%S')))
        dbconn.commit()
        
def get_recipients():
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        results = cur.execute('SELECT nom_addr FROM tb_emails')
    
    return [result[1] for result in results]


# In[6]:

get_recipients()

