
# coding: utf-8

# In[ ]:

import pkntbasics
import email
from imaplib import IMAP4_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.parser import Parser
import os
import smtplib
import sqlite3
import time


# In[ ]:

logger = pkntbasics.MAILLOGGER

POPSERVER = os.environ['POPSERVER']
SMTPSERVER = os.environ['SMTPSERVER']
SMTPPORT = int(os.environ['SMTPPORT'])
USER = os.environ['USER']
PASS = os.environ['PASS']


# In[ ]:

def fetch_emails(imap_conn, subject):
    '''
    fetch_emails(imap_conn, subject)
    imap_conn: A ssl.SSLContext object. For example, the returned value from pop_connection
    subject: The email subject to be searched
    
    Returns emails: A dict where the keys are the message ids and the values are email adresses
    '''
    global logger
    
    # Lists all messaages on the server where HEADER.SUBJECT is subject 
    _, ids = imap.uid('search', None, '(subject "{}")'.format(subject))
    # The return value is a tuple where the second element is a list containing the ids as a space separated string
    ids = ids[0].split()
    logger.debug('Found {} emails with subject "{}"'.format(len(ids), subject))
    emails = {}
    # Loops through the ids list
    for id in ids:
        logger.debug('Fetching email id ', id)
        # Fetches the FROM address
        _, res = imap.uid('fetch', id, 'BODY[HEADER.FIELDS (FROM)]')
        # The result is a tuple where the second element is a list of tuples
        # I know, it's complicated... Blame on imaplib!...
        _, res = res[0]
        # Decodes from bytes to string
        res = res.decode('utf-8')
        res = res[5:].strip() # Removes 'From:' at the beginning of the string
        logger.debug('id: {}, email: {}'.format(id, res))
        emails[id] = res
    
    return emails


def get_emails(server, user, pass_):
    with IMAP4_SSL(server) as imap:
        imap.login(user, pass_)
        imap.select("INBOX")

        emails_to_insert = fetch_emails(imap, "entrar")
        emails_to_remove = fetch_emails(imap, "sair")
    
    selected_emails = dict(IN=emails_to_insert,
                           OUT=emails_to_remove)
    
    return selected_emails

def remove_emails(server, user, pass_, uids):
    with IMAP4_SSL(IMAPSERVER) as imap:
        imap.login(USER, PASS)
        imap.select("[Gmail]/Lixeira")
        imap.uid('STORE', uids, '+FLAGS', r'\Deleted')
    

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
        <p>{0[description]}</p>
        <p>
           <b>Click <a href="https://www.packtpub.com/packt/offers/free-learning">here</a> to download.</b>
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


def smtp_connection(server, port, user, pass_):   
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
    smtp_conn.close()

