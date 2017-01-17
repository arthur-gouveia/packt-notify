
# coding: utf-8

# In[ ]:

import pkntbasics
import os
import pkntbook
import pkntemail
import pkntdb


# In[ ]:

SMTPSERVER = os.environ['SMTPSERVER']
SMTPPORT = int(os.environ['SMTPPORT'])
USER = os.environ['USER']
PASS = os.environ['PASS']
BOTKEY = os.environ['BOTKEY']


# In[ ]:

def telegram_notify(botkey, book):
    import telepot
    
    title = 'The free Packtpub book of today is *{0[name]}*'.format(book)
    link = 'Visit https://www.packtpub.com/packt/offers/free-learning to download'
    image = book['coverimage'].replace(' ', '%20')

    bot = telepot.Bot(botkey)
    bot.sendMessage('@packtpubnotify', title, 'Markdown')
    bot.sendPhoto('@packtpubnotify', image)
    bot.sendMessage('@packtpubnotify', link, disable_web_page_preview=True)


# In[ ]:

URL = 'https://www.packtpub.com/packt/offers/free-learning'
LOGLEVEL = 'WARNING'

logger = pkntbasics.get_logger(LOGLEVEL, 'Packt-Notify')

pkntbasics.config_loggers(LOGLEVEL)

book = pkntbook.get_book(URL)
conn = pkntemail.smtp_connection(SMTPSERVER, SMTPPORT, USER, PASS)

recipients = pkntdb.get_recipients()

pkntemail.send_book(book, conn, USER, recipients)

telegram_notify(BOTKEY, book)

conn.quit()

