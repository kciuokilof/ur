# -*- coding: utf-8 -*-

import sqlite3
import nltk
import sys
sys.path.append('../lib') # C:\Users\Kamil\PycharmProjects\Pobieranie_zawartosci_forum\lib
import sqlite3
sys.path.append('../src')
import numpy as np
from matplotlib import pyplot as plt



with open("unique_emos_codeing.txt", encoding="utf8") as f:
    infile_emos = f.read().splitlines()
with open("unique_tags_codeing.txt", encoding="utf8") as f:
    infile_tags = f.read().splitlines()


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
                print ('found')
                print (html_code)
                unique_emos.append(html_code)
    print(unique_emos)
    thefile = open('unique_tags3.txt', 'w')
    for item in unique_emos:
        thefile.write("%s\n" % item)


def replace_html_code1(line):
    if line in infile_emos:
        return chr(500 + line.index(line))
    elif line in infile_tags:
        return chr(402 + line.index(line))
    else:
        return chr(401)


def replace_html_code(line):
    for emos in infile_emos:
        if emos.find(line) != -1:
            return chr(500 + line.index(line))
    for emos in infile_tags:
        if emos.find(line) != -1:
            return chr(402 + line.index(line))
    return chr(401)

def process_html(answer):
    t2 = 0
    while answer.find('&quot;') != -1:
        t1 = answer.find('&quot;')
        t2 = t1+len("&quot;")
        replace_code = '"'
        answer = answer[:t1] + replace_code + answer[t2:]
    while answer.find('<') != -1:
        t1 = answer.find('<')
        t2 = answer.find('>') + 1
        if t2 == 0:
            return '-1'
        else:
            html_code = answer[t1:t2]
            replace_code = replace_html_code(html_code)
            answer =  answer[:t1]  +replace_code + answer[t2:]
    return answer

def text_tochar_user(user):
    conn = sqlite3.connect('C:\\Users\\Kamil\\Desktop\\studia\\Magisterka\\parrarel3\\posts.db')
    c = conn.cursor()
    c.execute("SELECT answer, id FROM posts WHERE user = '"+user+"';")

    conn.commit()
    answers = [[x[0], x[1]] for x in c]
    #  answers = ['ał', 'aŁ', '<<$>ąęłżźó$&€ a,9']
    text_data_decoded = []
    for idx, answer in enumerate(answers):
        sentences_list = []
        sentences_list.extend(nltk.sent_tokenize(answer))
        for sentance in sentences_list:
            answer_withouthtml = process_html(sentance[0])
            hex_values = ["{:02x}".format(ord(c)) for c in answer_withouthtml]
            decimal_values = [str(int(hex, 16)) for hex in hex_values]
            text_data_decoded.append(decimal_values)
            conn.execute("INSERT INTO posts_int (fid,answer) VALUES(?,?)", (answer[1],
                                                                        ' '.join(decimal_values)))
            conn.commit()


def text_chartoint():
#    select answer, user from posts where user = 'yasiek' or user = 'Łosiu'
    conn = sqlite3.connect('C:\\Users\\Kamil\\Desktop\\studia\\Magisterka\\parrarel3\\posts.db')
    c = conn.cursor()
  #  c.execute("CREATE TABLE 'posts_int' ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `fid` INTEGER, `answer` TEXT)")
    c.execute("SELECT  user, count(*) as ilosc FROM  posts GROUP BY user ORDER BY ilosc desc LIMIT 10;")
    conn.commit()
    users = [x[0] for x in c]
    conn.commit()
    for user in users[1:]:
        text_tochar_user(user)


def revert_from_int_to_char(text_data_decoded):
    print(text_data_decoded)
    rebuild = []
    for sentance in text_data_decoded:
        sentance_rebuild = str()
        for sign in sentance:
            sentance_rebuild = sentance_rebuild + chr(sign)
        rebuild.append(sentance_rebuild)
    print(rebuild)


def code_html_codes():
    unique_emoticons = set()
    unique_tags = set()
    others = set()
    with open("unique_tags.txt", encoding="utf8") as infile:
        for line in infile:
            if -1 == line.find('<'):
                continue
            elif 20 > len(line):
                content = line
                unique_tags.add(content)
            elif -1 != line.find('<img src="images'):
                content = line
                unique_emoticons.add(content)
            else:
                others.add(line)
    return unique_tags, unique_emoticons, others


def save_coding():
    unique_tags, unique_emoticons, others = code_html_codes()
    thefile = open('unique_emos_codeing.txt', 'w')
    for item in list(unique_emoticons):
         thefile.write("%s\n" % item.encode("utf-8"))
    thefile.close()
    thefile = open('unique_tags_codeing.txt', 'w')
    for item in list(unique_tags):
         thefile.write("%s\n" % item.encode("utf-8"))
    thefile.close()

def count_dft_of_sentace_length():
    username = 'dwiecegly'
    conn = sqlite3.connect('C:\\Users\\Kamil\\Desktop\\studia\\Magisterka\\parrarel2\\posts'
                           '.db')
    c = conn.cursor()
    c.execute("SELECT answer, date, time from posts;")
    # c.execute("SELECT answer, date, time from posts where user = ?;", (username,))
    conn.commit()
    answers = [x[0] for x in c]
    sentace_length = []
    sentences_withouthtml = []
    sentences_list = []
    for answer in answers[:1000]:
        sentences_list.extend(nltk.sent_tokenize(answer))
    for sentence in sentences_list:
        sentences_withouthtml.append(process_html(sentence))
    for sentence in sentences_withouthtml:
        if len(sentence) > 500:
            print('\nSentance\n')
            print(sentence)
        sentace_length.append(len(sentence))
    set_of_unique_sentances_length = list(set(sentace_length))
    set_of_unique_sentances_length.sort()
    sentace_length_count = []

    for unique_length in set_of_unique_sentances_length:
        sentace_length_count.append(sentace_length.count(unique_length))
    plt.plot(set_of_unique_sentances_length, sentace_length_count)
    plt.show()
#
# count_dft_of_sentace_length()
# text_chartoint()