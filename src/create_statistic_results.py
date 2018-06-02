import multiprocessing
import concurrent.futures
import itertools
import sys
sys.path.append('../lib') # C:\Users\Kamil\PycharmProjects\Pobieranie_zawartosci_forum\lib
import download_data
import sqlite3
import unidecode
from random import randint
from os import listdir
from os.path import isfile, join


mypath = 'C:\Users\Kamil\Desktop\studia\Magisterka\parrarel'

#SELECT  user, count(*) as ilosc FROM  posts GROUP BY user ORDER BY ilosc ASC LIMIT 10;



onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

conn = sqlite3.connect('C:\Users\Kamil\Desktop\studia\Magisterka\parrarel\posts10'
                       '.db')
web_url = 'http://forum.muratordom.pl'
threads_list = []
c = conn.cursor()
c.execute(

    "SELECT answer, user FROM  'posts' WHERE id <3;")
conn.commit()
resultuple_list = []
resultuple = c.fetchone()
resultuple_list.append(resultuple)
users = []
text_len_list = []
for row in c:
    text = row[0]
    user = row[1]
    t1 = text.find('<')
    if user in users:
        index = users.index(user)
    else:
        index = -1
        users.append(user)
        text_len_list.append(0)
    while t1 != -1:
        t1 = text.find('<')
        t2 = text.find('>')
        text1 = text[:t1]+text[t2:]
        text = text1
        t1 = text.find('<')
    text_len_list[index] = text_len_list[index] + len(text1)
print text_len_list


