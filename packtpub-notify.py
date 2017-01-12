
# coding: utf-8

# In[1]:

import pkntbasics
import os
import pkntbook
import pkntemail


# In[2]:

SMTPSERVER = os.environ['SMTPSERVER']
SMTPPORT = int(os.environ['SMTPPORT'])
USER = os.environ['USER']
PASS = os.environ['PASS']


# In[3]:

URL = 'https://www.packtpub.com/packt/offers/free-learning'
LOGLEVEL = 'WARNING'

logger = pkntbasics.get_logger(LOGLEVEL, 'Packt-Notify')

pkntbasics.config_loggers(LOGLEVEL)

book = pkntbook.get_book(URL)
conn = pkntemail.smtp_connection(SMTPSERVER, SMTPPORT, USER, PASS)
pkntemail.send_book(book, conn, USER, ', '.join(['gouveia.arthur@gmail.com','rodolfo.sousa.ti@gmail.com']))
conn.quit()

