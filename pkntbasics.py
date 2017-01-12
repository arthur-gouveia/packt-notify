
# coding: utf-8

# In[1]:

BOOKLOGGER = None
MAILLOGGER = None
DBLOGGER = None

def config_loggers(lvl):
    global BOOKLOGGER
    global MAILLOGGER
    global DBLOGGER
    
    BOOKLOGGER = get_logger(lvl, 'pkntbook')
    MAILLOGGER = get_logger(lvl, 'pkntmail')
    DBLOGGER = get_logger(lvl, 'pkntdb')
    

def get_logger(lvl, alias):
    import logging
    
    logger = logging.getLogger(alias)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-15s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(lvl)
    
    return logger

def create_database():
    import sqlite3
    
    with sqlite3.connect('packt-notify.db') as dbconn:
        cur = dbconn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS tb_books(
                        id_book INTEGER PRIMARY KEY ASC,
                        nom_book TEXT NOT NULL,
                        dt_fetched DATETIME NOT NULL)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS tb_emails
                     (id_addr INTEGER PRIMARY KEY ASC,
                      nom_addr TEXT NOT NULL,
                      dt_in DATE NOT NULL,
                      dt_out DATE,
                      id_last_book INT,
                      FOREIGN KEY(id_last_book) REFERENCES tb_books(id_book))''')
        dbconn.commit()

