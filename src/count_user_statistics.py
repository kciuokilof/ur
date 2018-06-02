# -*- coding: utf-8 -*-
import nltk
import sys
sys.path.append('../lib') # C:\Users\Kamil\PycharmProjects\Pobieranie_zawartosci_forum\lib
import process_data
import sqlite3
sys.path.append('../src')
import numpy as np
from matplotlib import pyplot as plt


def count_user_posts_number_statistic():
    db_names_list = ['C:\\Users\\Kamil\\Desktop\\studia\\Magisterka\\parrarel3\\posts.db']
    conn = sqlite3.connect(db_names_list[0])
    c = conn.cursor()
    c.execute("SELECT  user, count(*) as ilosc FROM  posts GROUP BY user ORDER BY ilosc asc")
    conn.commit()
    users_count = [x[1] for x in c]
    set_of_unique_user_posts_num = list(set(map(int, users_count)))
    set_of_unique_user_posts_num.sort()
    sentace_length_count = []
    for unique_length in set_of_unique_user_posts_num:
        sentace_length_count.append(users_count.count(unique_length))
    plt.plot(set_of_unique_user_posts_num, sentace_length_count, 'ro')
    plt.show()


def count_top_users_sentace_length_statistic():
    db_names_list = ['C:\\Users\\Kamil\\Desktop\\studia\\Magisterka\\parrarel3\\posts.db']
    conn = sqlite3.connect(db_names_list[0])
    c = conn.cursor()
    c.execute("SELECT  user, count(*) as ilosc FROM  posts GROUP BY user ORDER BY ilosc desc LIMIT 5;")
    conn.commit()
    users = [x[0] for x in c]
    for idx, user in enumerate(users[1:]):
        number_of_rows_saved = 0
        print(str(idx))
        c = conn.cursor()
        c.execute("SELECT  answer  FROM  posts where user = '"+user+"' ORDER BY id  desc LIMIT 11000")
        answers = [x[0] for x in c]
        c.close()
        sentences = []
        for idx3, answer in enumerate(answers):
            answer_withouthtml = process_data.process_html(answer)
            sentences.append(answer_withouthtml)
            #sentences.extend(nltk.sent_tokenize(answer_withouthtml))
        sentace_length = []

        for sentence in sentences:
            sentace_length.append(len(sentence))
        set_of_unique_sentances_length = list(set(sentace_length))
        set_of_unique_sentances_length.sort()
        sentace_length_count = []

        for unique_length in set_of_unique_sentances_length:
            sentace_length_count.append(sentace_length.count(unique_length))
        plt.plot(set_of_unique_sentances_length, sentace_length_count)
    plt.show()


def count_sentace_length_statistic():

    username = 'dwiecegly'
    conn = sqlite3.connect('C:\\Users\\Kamil\\Desktop\\studia\\Magisterka\\parrarel2\\posts'
                           '.db')
    c = conn.cursor()
    c.execute("SELECT answer, date, time from posts;")
    #c.execute("SELECT answer, date, time from posts where user = ?;", (username,))
    conn.commit()
    answers = [x[0] for x in c]
    sentences= []
    for answer in answers[:40000]:
        answer_withouthtml = process_data.process_html(answer)
        sentences.append(answer_withouthtml)
        #sentences.extend(nltk.sent_tokenize(answer_withouthtml))
    sentace_length = []

    for sentence in sentences:
        sentace_length.append(len(sentence))
    set_of_unique_sentances_length = list(set(sentace_length))
    set_of_unique_sentances_length.sort()
    sentace_length_count = []

    for unique_length in set_of_unique_sentances_length:
        sentace_length_count.append(sentace_length.count(unique_length))
    plt.plot(set_of_unique_sentances_length, sentace_length_count)
    plt.show()

def find_maximum_length():
    conn = sqlite3.connect('C:\\Users\\Kamil\\Desktop\\studia\\Magisterka\\parrarel2\\posts'
                           '.db')
    c = conn.cursor()
    c.execute("SELECT answer, date, time from posts;")
    # c.execute("SELECT answer, date, time from posts where user = ?;", (username,))
    conn.commit()
    answers = [x[0] for x in c]
    sentences = []
    for answer in answers[:10000]:
        sentences.extend(nltk.sent_tokenize(answer))
    sentace_length = []
    for sentence in sentences:
        sentace_length.append(len(sentence))
    set_of_unique_sentances_length = list(set(sentace_length))
    set_of_unique_sentances_length.sort()


def find_unique_emos():
    conn = sqlite3.connect('C:\\Users\\Kamil\\Desktop\\studia\\Magisterka\\parrarel3\\posts.db')
    conn.text_factory = str
    c = conn.cursor()
    c.execute("select answer from posts;")
    conn.commit()
    answers = [x[0] for x in c]
   # answers = ['<costam>']
    unique_emos = []
    for answer in answers:
        t2 = 0
        while answer.find('<', t2) != -1:
            t1 = answer.find('<',t2)
            t2 = answer.find('>',t1) + 1
            html_code = answer[t1:t2]
            html_code.replace('\n','')
            if not html_code in unique_emos:
                print('found')
                print(html_code)
                unique_emos.append(html_code)
    print(unique_emos)
    thefile = open('unique_tags3.txt', 'w')
    for item in unique_emos:
        thefile.write("%s\n" % item)


#count_sentace_length_statistic()
count_user_posts_number_statistic()