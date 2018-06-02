# -*- coding: utf-8 -*-
import sys
import sqlite3
sys.path.append('../lib') # C:\Users\Kamil\PycharmProjects\Pobieranie_zawartosci_forum\lib
import download_data
from multiprocessing import Pool
import concurrent.futures


def download_posts(topic):
    threat_posts = []
    threads_list = []
    conn = sqlite3.connect('C:\Users\Kamil\Desktop\studia\Magisterka\posts.db')
    c = conn.cursor()
    c.execute("CREATE TABLE 'posts-'"+topic['title']+" ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `topic` TEXT NOT NULL, `thread` TEXT, `page` TEXT, `answer` TEXT, `user` TEXT, `time` TEXT, `date` TEXT )")
    conn.commit()
    topic_url = unicode(web_url + '/' + topic['href']).encode('utf-8')
    print topic_url
    threads = download_data.get_threads(topic_url)
    threads_list.extend(threads)
    for thread in threads_list[:]:
        thread_url = unicode(web_url + '/' + thread['href']).encode('utf-8')
        web_content = download_data.download_forum_subject(thread_url)
        download_data.safe_data_to_file(unicode(web_content).encode('utf-8'), file_path)
        web_pages_num = download_data.check_webpages_num(web_content)
        for web_page in range(1, web_pages_num + 1):
            proc_num = proc_num + 1
            webpage_url = unicode(web_url + '/' + thread['href'] + '/page' + str(web_page)).encode('utf-8')
            print thread_url + "\t" + webpage_url
            web_content = download_data.download_forum_subject(webpage_url)
            posts = download_data.split_subjects(web_content)
            for post in posts:
                post['topic'] = topic['title']
                post['thread'] = thread['title']
                post['page'] = web_page
                c.execute("INSERT INTO posts8 (topic,thread,page,answer,user,time,date) VALUES(?,?,?,?,?,?,?)",
                          (post['topic'],
                           post['thread'],
                           str(post['page']),
                           post['answer'],
                           post['users'],
                           post['time'],
                           post['date']))
                conn.commit()
    conn.close()


forum_url = 'http://forum.muratordom.pl/forum.php'
web_url = 'http://forum.muratordom.pl'
topics = download_data.get_topics('http://forum.muratordom.pl/forum.php')
url= 'http://forum.muratordom.pl/showthread.php?333872-Bocianki-2017-witamy-i-zapraszamy-)/page18'
file_path = '../files/test4.html'
web_content = download_data.download_forum_subject(url)
subjects = download_data.split_subjects(web_content)
conn = sqlite3.connect('C:\Users\Kamil\Desktop\studia\Magisterka\posts.db')
c = conn.cursor()
# c.execute("CREATE TABLE 'posts8' ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `topic` TEXT NOT NULL, `thread` TEXT, `page` TEXT, `answer` TEXT, `user` TEXT, `time` TEXT, `date` TEXT )")
conn.commit()
conn.close()
proc_num = 10000
executor = concurrent.futures.ProcessPoolExecutor(5)
futures = [executor.submit(download_posts, topic) for topic in topics[3:5]]
concurrent.futures.wait(futures)


