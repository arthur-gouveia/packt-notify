
# coding: utf-8

# In[1]:

import sqlite3


# In[2]:

with sqlite3.connect('packt-notify.db') as dbconn:
    cur = dbconn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tb_books(
                    id_book INT PRIMARY KEY NOT NULL,
                    nom_book TEXT NOT NULL,
                    dt_fetched DATATIME NO NULL)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS tb_emails
                 (id_addr INT PRIMARY KEY NOT NULL,
                  nom_addr TEXT NOT NULL,
                  dt_in DATE NOT NULL,
                  dt_out DATE,
                  id_last_book INT,
                  FOREIGN KEY(id_last_book) REFERENCES tb_books(id_book))''')
    dbconn.commit()

