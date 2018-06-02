import multiprocessing
import itertools
import sys
sys.path.append('../lib')
import download_data
import sqlite3
import unidecode


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = iterable * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)


def try_multiple_operations(topic):
    conn = sqlite3.connect('C:\Users\Kamil\Desktop\studia\Magisterka\parrarel3\posts4.db',timeout=35.0)
    web_url = 'http://forum.muratordom.pl'
    print unidecode.unidecode(topic['title'])
    threads_list = []
   # c = conn.cursor()
   # c.execute("CREATE TABLE 'posts' ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `topic` TEXT NOT NULL, `thread` TEXT, `page` TEXT, `answer` TEXT, `user` TEXT, `time` TEXT, `date` TEXT )")
   # conn.commit()
    topic_url = unicode(web_url + '/' + topic['href']).encode('utf-8')
    print topic_url
    threads_list = download_data.get_threads(topic_url)
    insert_coutner = 0
    for thread in threads_list[:]:
        thread_url = unicode(web_url + '/' + thread['href']).encode('utf-8')
        web_content = download_data.download_forum_subject(thread_url)
        web_pages_num = download_data.check_webpages_num(web_content)
        for web_page in range(1, web_pages_num + 1):
            webpage_url = unicode(web_url + '/' + thread['href'] + '/page' + str(web_page)).encode('utf-8')
           # print webpage_url
            try:
                web_content = download_data.download_forum_subject(webpage_url)
            except Exception as e:
                print (str(e))
                print('ERROR!')
                print   webpage_url
                web_content = "Error"
                return []
            posts = download_data.split_subjects(web_content)
            for post in posts:
                post['topic'] = topic['title']
                post['thread'] = thread['title']
                post['page'] = web_page
                try:
                    conn.execute("INSERT INTO posts (topic,thread,page,answer,user,time,date) VALUES(?,?,?,?,?,?,?)",
                          (post['topic'],
                           post['thread'],
                           str(post['page']),
                           post['answer'],
                           post['users'],
                           post['time'],
                           post['date']))

                except Exception as e:
                    print('ERROR2! found near: '+ webpage_url)
                    print e


            conn.commit()
    conn.close()

    print('\nDone\n'+unidecode.unidecode(topic['title']))


if __name__ == '__main__':
    # conn = sqlite3.connect('C:\Users\Kamil\Desktop\studia\Magisterka\parrarel3\posts3.db')
    # conn.execute(
    #     "CREATE TABLE 'posts' ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `topic` TEXT NOT NULL, `thread` TEXT, `page` TEXT, `answer` TEXT, `user` TEXT, `time` TEXT, `date` TEXT )")
    # conn.commit()
    # conn.close()
    topics = download_data.get_topics('http://forum.muratordom.pl/forum.php')
   # threads = download_data.get_threads('http://forum.muratordom.pl/'+topics[4]['href'])
   # try_multiple_operations(topics[0])
    pool = multiprocessing.Pool(processes=12)
    try:
        pool.map(try_multiple_operations, topics)
    except Exception as e:
        print(str(e))