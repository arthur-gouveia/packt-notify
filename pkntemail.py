
# coding: utf-8

# In[29]:

import pkntbasics
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import poplib
import sqlite3
import time


# In[22]:

logger = pkntbasics.MAILLOGGER

POPSERVER = os.environ['POPSERVER']
SMTPSERVER = os.environ['SMTPSERVER']
SMTPPORT = int(os.environ['SMTPPORT'])
USER = os.environ['USER']
PASS = os.environ['PASS']


# ```A logica aqui e' buscar os novos emails
# Verificar os emails a descadastrar e fazer o cancelamento
# Verificar os emails a cadastrar e enviar o livro atual
#     Se enviou com sucesso cadastrar o email com o id do livro
#     Se falhou o envio cadastrar o email com o id NULL```

# In[25]:

def pop_connection(server, user, pass_):
    '''
    pop_connection(popserver, user, pass_)
    server: string - Address of the server to connecto to
    user:   string - Username for login
    pass_:  string - Password for login
    
    Returns pop_conn: A ssl.SSLContext object
    
    Connects to a pop3 server through SSL and returns the connection - ans ssl.SSLContext object
    
    
    Example:
    
    >>> import pkntemail
    >>> conn = pkntemail.pop_connection(POPSERVER, USER, PASS)
    >>> conn.getwelcome() #doctest: +ELLIPSIS
    b'+OK ... ready for requests ...'
    >>> conn.context #doctest: +ELLIPSIS
    <ssl.SSLContext object at 0x...>
    >>> conn.quit()
    b'+OK Farewell.'
    '''
    logger.debug('Connecting to '+server)
    pop_conn = poplib.POP3_SSL(server)
    try:
        logger.debug('Log in')
        pop_conn.user(user)
        pop_conn.pass_(pass_)
    except poplib.error_proto:
        logger.error('Authentication failed for user '+user)
        pop_conn.quit()
        return poplib.error_proto
    else:
        return pop_conn


def smtp_connection(server, port, user, pass_):
    import smtplib
    
    '''
    pop_connection(popserver, user, pass_)
    server: string - Address of the server to connecto to
    user:   string - Username for login
    pass_:  string - Password for login
    
    Returns pop_conn: A ssl.SSLContext object
    
    Connects to a pop3 server through SSL and returns the connection - ans ssl.SSLContext object
    
    
    Example:
    
    >>> import pkntemail
    >>> conn = pkntemail.pop_connection(POPSERVER, USER, PASS)
    >>> conn.getwelcome() #doctest: +ELLIPSIS
    b'+OK ... ready for requests ...'
    >>> conn.context #doctest: +ELLIPSIS
    <ssl.SSLContext object at 0x...>
    >>> conn.quit()
    b'+OK Farewell.'
    '''
    
    logger.debug('Connecting to '+server)
    smtp_conn = smtplib.SMTP(server, port)
    try:
        logger.debug('Log in')
        smtp_conn.starttls()
        smtp_conn.login(user, pass_)
    except smtplib.SMTPConnectError:
        logger.error('Authentication failed for user '+user)
        smtp_conn.quit()
        return smtplib.SMTPConnectError
    else:
        return smtp_conn

def fetch_emails(pop_conn):
    '''
    fetch_emails(pop_conn)
    pop_conn: A ssl.SSLContext object. For example, the returned value from pop_connection
    
    Returns messages: A dict where the keys are the message ids and the values are email.message objects
    '''
    from email.parser import Parser
    
    global logger
    # Lists all the messages on the server
    _, items, _ = pop_conn.list()
    logger.info('Retrieved %d items from server' %len(items))
    # Retrieves the messages
    messages = {i: pop_conn.retr(i) for i in range(1, len(items)+1)}
    # Decodes from bytes to strings
    messages = {key: [m.decode() for m in messages[key][1]] for key in messages.keys()}
    # Joins all the list strings in a large string separated by a newline \n
    messages = {key: '\n'.join(messages[key]) for key in messages.keys()}
    # Parses the strings to an email.message object
    messages = {key: Parser().parsestr(messages[key]) for key in messages.keys()}
    
    return messages


def select_emails(pop_conn):
    messages = fetch_emails(pop_conn)
    
    selected_emails = {}
    emails_to_insert = set()
    emails_to_remove = set()
    
    for message in messages:
        action = message['Subject']
        if 'entrar' in action.lower():
            emails_to_inser.add(message['From'])
        if 'sair' in action.lower():
            emails_to_remove.add(message['From'])
        selected_emails['in'] = emails_to_insert
        selected_emails['out'] = emails_to_remove
    
    return selected_emails


def send_book(bookdict, smtp_conn, from_, to):
    msg = create_book_message(bookdict)
        
    msg['Subject'] = "Free Book - {0[name]}".format(bookdict)
    msg['From'] = from_
    msg['To'] = 'Undisclosed Recipients <packtpubnotify@gmail.com>'
   
    while True:
        results = to.fetchmany(100)
        if not results:
            break
        else:
            adresses = [result[0] for result in results]
            msg['Bcc'] = ', '.join(adresses)
    
    smtp_conn.send_message(msg)


def create_book_message(bookdict):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')

    # Create the body of the message (a plain-text and an HTML version).
    text = "The PacktPub free book of the day is {0[name]}\n\nClick here to download:\nhttps://www.packtpub.com/packt/offers/free-learning".format(bookdict)
    html = """
    <html>
      <head></head>
      <body>
        <h2>The free PacktPub book of the day is {0[name]}</h2>
        <img src="{0[coverimage]}"><br>
        <p>{0[description]}<br>
           Click <a href="https://www.packtpub.com/packt/offers/free-learning">here</a> to download.
        </p>
      </body>
    </html>
    """.format(bookdict)

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    return msg


# pop_conn = pop_connection(POPSERVER, USER, PASS)
# messages = select_emails(pop_conn)
# pop_conn.quit()
#     
# for id, message in messages.items():
#     email_addr = message['From']
#     logger.debug('Email to insert '+email_addr)
#     action = message['Subject']
#     logger.debug('Action to perform '+action)
#     if 'entrar' in action.lower():
#         try:
#             logger.debug('Trying to send email')
#             if send_book(email_addr):
#                 logger.debug('Email sent succesfully')
#                 id_livro, nome_livro = get_last_book()
#                 logger.debug('Last book is '+nome_livro)
#             else:
#                 id_livro = none
#             sign_up(email_addr, id_livro)
#         except:
#             logger.debug('Unable to delete message '+str(id))
#             print('Unable to delete message.')
#         finally:
#             conexão_pop.quit()
#             logger.debug('Closed the connection')

# smtp_conn.quit()

# smtp_conn = smtp_connection(SMTPSERVER, SMTPPORT, USER, PASS)
