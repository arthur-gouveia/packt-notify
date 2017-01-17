
# coding: utf-8

# In[ ]:

import pkntbasics
import os
import pkntbook
import pkntemail
import pkntdb
import pkntbot


# In[ ]:

SMTPSERVER = os.environ['SMTPSERVER']
SMTPPORT = int(os.environ['SMTPPORT'])
USER = os.environ['USER']
PASS = os.environ['PASS']
BOTKEY = os.environ['BOTKEY']


# In[ ]:

URL = 'https://www.packtpub.com/packt/offers/free-learning'
LOGLEVEL = 'WARNING'

logger = pkntbasics.get_logger(LOGLEVEL, 'Packt-Notify')

pkntbasics.config_loggers(LOGLEVEL)

book = pkntbook.get_book(URL)
conn = pkntemail.smtp_connection(SMTPSERVER, SMTPPORT, USER, PASS)

recipients = pkntdb.get_recipients()

pkntemail.send_book(book, conn, USER, recipients)

pkntbot.telegram_notify(BOTKEY, book)

conn.quit()

