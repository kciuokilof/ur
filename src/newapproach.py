import multiprocessing
import concurrent.futures
import itertools
import sys
sys.path.append('../lib') # C:\Users\Kamil\PycharmProjects\Pobieranie_zawartosci_forum\lib
import download_data
import sqlite3
import unidecode
from random import randint


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = iterable * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def try_multiple_operations(topic):
    seed = randint(1, 100)
    conn = sqlite3.connect('C:\Users\Kamil\Desktop\studia\Magisterka\parrarel\posts'+unidecode.unidecode(topic['title'][0:9])+str(seed)+'.db')
    web_url = 'http://forum.muratordom.pl'
    print unidecode.unidecode(topic['title'][0:5])
    threads_list = []
    c = conn.cursor()
    c.execute("CREATE TABLE 'posts' ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `topic` TEXT NOT NULL, `thread` TEXT, `page` TEXT, `answer` TEXT, `user` TEXT, `time` TEXT, `date` TEXT )")
    conn.commit()
    topic_url = unicode(web_url + '/' + topic['href']).encode('utf-8')
    print topic_url
    threads = download_data.get_threads(topic_url)
    threads_list.extend(threads)
    for thread in threads_list[:]:
        thread_url = unicode(web_url + '/' + thread['href']).encode('utf-8')
        web_content = download_data.download_forum_subject(thread_url)
        web_pages_num = download_data.check_webpages_num(web_content)
        for web_page in range(1, web_pages_num + 1):
            webpage_url = unicode(web_url + '/' + thread['href'] + '/page' + str(web_page)).encode('utf-8')
            print webpage_url
            try:
                web_content = download_data.download_forum_subject(webpage_url)
            except:
                print('ERROR!')
                print   webpage_url
                web_content = "Error"
            posts = download_data.split_subjects(web_content)
            for post in posts:
                post['topic'] = topic['title']
                post['thread'] = thread['title']
                post['page'] = web_page
                try:
                    c.execute("INSERT INTO posts (topic,thread,page,answer,user,time,date) VALUES(?,?,?,?,?,?,?)",
                          (post['topic'],
                           post['thread'],
                           str(post['page']),
                           post['answer'],
                           post['users'],
                           post['time'],
                           post['date']))
                    conn.commit()
                except:
                    print('ERROR2!')
                    print   webpage_url
    conn.close()


if __name__ == '__main__':
    topics = download_data.get_topics('http://forum.muratordom.pl/forum.php')
    pool = multiprocessing.Pool(processes=16)
    try:
        pool.map(try_multiple_operations, topics)
    except Exception:
        pass