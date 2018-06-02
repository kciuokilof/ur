# -*- coding: utf-8 -*-
import xml.etree.ElementTree as et
import sys
import sqlite3
import csv
import nltk
import codecs, os
import re
import string
import gc
from langdetect import detect
import subprocess
sys.path.append('../lib')
import process_data as proc
from bs4 import BeautifulSoup
from string import punctuation
def strip_punctuation(s):
    return ''.join(c for c in s if c not in punctuation)


path_to_skigram_v2 ="C:\\Users\\Kamil\\Desktop\\studia\\ED\\skipgram\\skip_gram_v102m8.w2v.txt"
db_names_list = ['C:\\Users\\Kamil\\Desktop\\studia\\Magisterka\\parrarel3\\posts.db']
conn = sqlite3.connect(db_names_list[0])
c = conn.cursor()
c.execute("SELECT  user, count(*) as ilosc FROM  posts GROUP BY user ORDER BY ilosc desc LIMIT 3 OFFSET 1;")
conn.commit()
users = [x[0] for x in c]
replace_codes =['kowalski::noun', 'tag::noun']
path_to_taikip = 'C:\\Users\\Kamil\\Desktop\\studia\\ED\\TaKIPI18\\TaKIPI18\\Windows\\'
workspace_dir = 'C:\\Users\\Kamil\\PycharmProjects\\Pobieranie_zawartosci_forum\\src\\'
txt_processed_posts = workspace_dir+'forumpedia_csv\\txt_processed_posts.txt'
txt_file_char_model_train = workspace_dir+'forumpedia_csv\\char_model_train.txt'
txt_file_w2v_model_train = workspace_dir+'forumpedia_csv\\w2v_model_train.txt'
txt_file_text_reference = workspace_dir+'forumpedia_csv\\text_reference_train.txt'
os.chdir(path_to_taikip)

finishes_tweets_cntr = 0
unrecognised_tweets_cntr = 0


def prepare_csv_for_char_model(answer):
    answer_withouthtml = proc.process_html(answer)
    if answer_withouthtml == '-1':
        print('unrecognized char model sentace')
        return False
    sentences = nltk.sent_tokenize(answer_withouthtml)
    for sentance in sentences:
        if 20 < len(sentance) < 220:
            hex_values = ["{:02x}".format(ord(c)) for c in sentance]
            decimal_values = [int(hex, 16) for hex in hex_values]
            if max(decimal_values) > 600:
                print('unrecognized char model post')
                continue
            else:
                print('recognized char model post')
                return [str(int(hex, 16)) for hex in hex_values]

def prepare_csv_for_w2v_model(tweet):
    global finishes_tweets_cntr
    global unrecognised_tweets_cntr
    file = codecs.open(path_to_taikip+"in.txt", "w", "utf-8")
    tweet = re.sub(r'http\S+', '', tweet)
    soup = BeautifulSoup(tweet)
    tweet = ''.join(soup.findAll(text=True))
    file.write(tweet) #u'\ufeff')
    file.close()
    subprocess.call(path_to_taikip+"takipi.exe -it TXT -i in.txt -o out.xml -force one -old")
    tree = et.parse(path_to_taikip+'out.xml')
    lemm_words_list = []
    leksykal_tag_list = []
    lemm_one_word_list = []
    org_words_list = []
    tweet_acount_tag = 0
    for elem in tree.iter():
        if elem.tag == 'orth':
            org_words_list.append(strip_punctuation(elem.text))
    org_words_list = list(filter(None, org_words_list))
    for elem in tree.iter():
        if elem.tag == 'tok':
            lemm_words_list.append(lemm_one_word_list)
            lemm_one_word_list = []
#Adding best result on the beggingin of the list
        if elem.tag=='lex' and len(elem.attrib) == 1:
            lemm_word = elem
            if "subst" in lemm_word[1].text or "ppron" in lemm_word[1].text:
                leksykal_tag = 'noun'
                leksykal_tag_list.append(leksykal_tag)
                if tweet_acount_tag != 0:
                    lemm_one_word_list = [replace_codes[tweet_acount_tag-1]] + lemm_one_word_list
                lemm_one_word_list = [lemm_word[0].text+"::"+leksykal_tag]+lemm_one_word_list
            elif "perf" in lemm_word[1].text:
                leksykal_tag = 'verb'
                leksykal_tag_list.append(leksykal_tag)
                if tweet_acount_tag != 0:
                    lemm_one_word_list = [replace_codes[tweet_acount_tag-1]] + lemm_one_word_list
                lemm_one_word_list = [lemm_word[0].text+"::"+leksykal_tag]+lemm_one_word_list

            elif "ign" in lemm_word[1].text or "qub" in lemm_word[1].text or "acc" in lemm_word[1].text or "gen" in lemm_word[1].text:
                leksykal_tag = ''
                leksykal_tag_list.append(leksykal_tag)
                if tweet_acount_tag != 0:
                    lemm_one_word_list = [replace_codes[tweet_acount_tag-1]] + lemm_one_word_list
                lemm_one_word_list = [lemm_word[0].text+"::"+leksykal_tag]+lemm_one_word_list

            elif "interp" in lemm_word[1].text:
                if lemm_word[0].text == '@':
                    tweet_acount_tag = 1
                if lemm_word[0].text == '#':
                    tweet_acount_tag = 2
            else: #prep adj
                leksykal_tag = lemm_word[1].text.split(":")[0]
                leksykal_tag_list.append(leksykal_tag)
                if tweet_acount_tag != 0:
                    lemm_one_word_list = [replace_codes[tweet_acount_tag-1]] + lemm_one_word_list
                lemm_one_word_list = [lemm_word[0].text+"::"+leksykal_tag]+lemm_one_word_list
#Adding other results on the end of the list
        elif elem.tag == 'lex':
            lemm_word = elem
            if "subst" in lemm_word[1].text or "ppron" in lemm_word[1].text:
                leksykal_tag = 'noun'
                leksykal_tag_list.append(leksykal_tag)
                lemm_one_word_list.append(lemm_word[0].text+"::"+leksykal_tag)
            elif "perf" in lemm_word[1].text:
                leksykal_tag = 'verb'
                leksykal_tag_list.append(leksykal_tag)
                lemm_one_word_list.append(lemm_word[0].text+"::"+leksykal_tag)
            elif "ign" in lemm_word[1].text or "qub" in lemm_word[1].text:
                leksykal_tag = ''
                leksykal_tag_list.append(leksykal_tag)
                lemm_one_word_list.append(lemm_word[0].text+"::"+leksykal_tag)
            elif "interp" in lemm_word[1].text:
                pass
            else: #prep adj
                leksykal_tag = lemm_word[1].text.split(":")[0]
                leksykal_tag_list.append(leksykal_tag)
                lemm_one_word_list.append(lemm_word[0].text+"::"+leksykal_tag)
    lemm_words_list.append(lemm_one_word_list)
    lemm_words_list_cleared = [x for x in lemm_words_list if x != []]

    if len(lemm_words_list_cleared)!=len(org_words_list):
        return False
    word2vec_list = []
    found_tag = 0
    for word_idx, word_plus_lex in enumerate(lemm_words_list_cleared):
        found_tag = 0
        with open(path_to_skigram_v2, encoding="utf-8") as fp:
            for line in fp:
                if line.lower().startswith(word_plus_lex[0]):
                    word2vec_list.append(line.split(" ")[1:])
                    found_tag = 1
                    break
            if found_tag == 0 and len(word_plus_lex) > 1:
                with open(path_to_skigram_v2, encoding="utf-8") as fp:
                    for line in fp:
                        if line.lower().startswith(word_plus_lex[1]):
                            word2vec_list.append(line.split(" ")[1:])
                            found_tag = 1
                            break
            if found_tag == 0 and len(word_plus_lex) > 2:
                with open(path_to_skigram_v2, encoding="utf-8") as fp:
                    for line in fp:
                        if line.lower().startswith(word_plus_lex[-1]):
                            word2vec_list.append(line.split(" ")[1:])
                            found_tag = 1
                            break
            if found_tag == 0:
                with open(path_to_skigram_v2, encoding="utf-8") as fp:
                    for line in fp:
                        if line.lower().startswith(org_words_list[word_idx][:-1]):
                            word2vec_list.append(line.split(" ")[1:])
                            found_tag = 1
                            break
        if found_tag == 0:
            unrecognised_tweets_cntr = unrecognised_tweets_cntr + 1
            print('unrecognised_w2v post:')
            return False
    word2vec_strings_list = []
    for word2vec in word2vec_list:
        word2vec_strings_list.append(' '.join(word2vec))

    word2vec_string = ','.join(word2vec_strings_list)
    if found_tag == 1:
        print('recognised_w2v post:')
        return  word2vec_string.replace('\n', '')+'\n'
    else:
        return False
users = users[0:2]
with open(txt_processed_posts, 'r', encoding="utf-8") as fp_read:
    already_processed_posts_list = fp_read.readlines()
    fp_read.close()
    already_processed_posts_list =[int(c.strip()) for c in already_processed_posts_list]

for idx, user in enumerate(users):
    number_of_rows_saved = 0
    print('\n\n\n################################USER:'+user + '########'
                                                               '        ###############################\n\n\n')
    c = conn.cursor()
    c.execute("SELECT  answer  FROM  posts where user = '"+user+"' ORDER BY id  desc ")
    answers = [x[0] for x in c]
    c.execute("SELECT  id  FROM  posts where user = '" + user + "' ORDER BY id  desc ")
    ids = [x[0] for x in c]
    c.close()
    gc.collect()
    for idx3, answer in enumerate(answers):
        if ids[idx3] not in already_processed_posts_list and 20<len(answer)<180:
            print('\n\n////////////////////////////Processing post//////////////////////////////////////\n' + answer)
            print('\n//////////////////////////////////////////////////////////////////////////////////////////////')
            with open(txt_processed_posts, 'a', encoding="utf-8") as fp_write:
                fp_write.write(str(ids[idx3]).strip() + '\n')
            char_model_output = prepare_csv_for_char_model(answer)
            w2v_model_output = prepare_csv_for_w2v_model(answer)
            if w2v_model_output and char_model_output:
                number_of_rows_saved = number_of_rows_saved + 1
                print('\n************************Post processing finished*************************\n' + str(number_of_rows_saved))

                with open(txt_file_char_model_train, 'a', encoding="utf-8") as fp_write:
                    fp_write.write(str(idx) + ':' + ' '.join(char_model_output)+'\n')
                with open(txt_file_w2v_model_train, 'a', encoding="utf-8") as fp_write:
                    fp_write.write(str(idx) + ':' + w2v_model_output)
                with open(txt_file_text_reference, 'a', encoding="utf-8") as fp_write:
                    fp_write.write(str(idx)+ ':' + str(ids[idx3]).strip() + ':' + answer +'\n')
                # writer = csv.writer(csv_file_char_model_train, delimiter=':')
                # writer.writerow([idx, ' '.join(char_model_output)])
                # writer = csv.writer(csv_file_w2v_model_train, delimiter=':')
                # writer.writerow([idx, csv_file_w2v_model_train])
                if number_of_rows_saved == 1000:
                    print(user+' done!!!')
                    break
            else:
                print('\n==========================Post processing fail===========================\n')