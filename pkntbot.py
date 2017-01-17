
# coding: utf-8

# In[ ]:

import pkntbasics
import telepot


# In[ ]:

pkntbasics.config_loggers('WARNING')
logger = pkntbasics.BOTLOGGER


# In[ ]:

def telegram_notify(botkey, book):   
    global logger
    
    title = 'The free Packtpub book of today is *{0[name]}*'.format(book)
    link = 'Visit https://www.packtpub.com/packt/offers/free-learning to download'
    image = book['coverimage'].replace(' ', '%20')

    bot = telepot.Bot(botkey)
    logger.debug('Created the bot')
    msg = bot.sendMessage('@packtpubnotify', title, 'Markdown')
    logger.debug('Sent book title: {!s}'.format(msg))
    msg = bot.sendPhoto('@packtpubnotify', image)
    logger.debug('Sent book cover image: {!s}'.format(msg))
    msg = bot.sendMessage('@packtpubnotify', link, disable_web_page_preview=True)
    logger.debug('Sent download link: {!s}'.format(msg))

