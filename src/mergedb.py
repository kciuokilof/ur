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


def merge_tables(db, conn2):
    conn1 = sqlite3.connect(mypath+'\\'+db)
    c2 = conn2.cursor()
    c1 = conn1.cursor()
    c1.execute(

        "SELECT topic, thread, page, answer, user, time, date FROM  'posts' ;")
    conn1.commit()
    resultuple_list = []
    resultuple = c1.fetchone()
    resultuple_list.append(resultuple)
    for row in c1:
    #if resultuple_list != [None]:
        c2.execute('INSERT INTO posts (topic,thread,page,answer,user,time,date) VALUES(?,?,?,?,?,?,?)', row)
        conn2.commit()



onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

conn = sqlite3.connect('C:\Users\Kamil\Desktop\studia\Magisterka\parrarel\posts10'
                       '.db')
web_url = 'http://forum.muratordom.pl'
threads_list = []
c = conn.cursor()
c.execute("CREATE TABLE 'posts' ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `topic` TEXT NOT NULL, `thread` TEXT, `page` TEXT, `answer` TEXT, `user` TEXT, `time` TEXT, `date` TEXT )")
for db in onlyfiles[:]:
    merge_tables(db, conn)
