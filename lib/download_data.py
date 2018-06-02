# -*- coding: utf-8 -*-
import requests
import re
from lxml import etree
import lxml.html


def download_forum_subject(url):
    req = requests.get(url)
    return req.text


def safe_data_to_file(webContent, file_name):
    f = open(file_name, 'w')
    f.write(webContent)
    f.close


def check_webpages_num(webContent):
    t1 = webContent.find("Strona 1 z ")
    t2 = webContent.find("</a>", t1)
    if t1 == -1:
        return 1
    return int(webContent[t1+len("Strona 1 z "):t2])

def get_digits(str1):
    c = ""
    for i in str1:
        if i.isdigit():
            c += i
    return c


def split_subjects(webContent,):
    pattern = re.compile('<div class="posthead">')
    subject_index = []
    subject_name = []
    subjects = []
    result = {unicode}
    start = 0
    for m in pattern.finditer(webContent):
        subject_index.append(m.start())
        subject_name.append(m.group())
        index = get_digits(m.group())
        subjects.append({'title': 'url', 'index': index, 'start_index': m.start()})
        if len(subjects) > 1:
            subjects[-2]['end_index'] = m.start()
    if len(subjects)!=0:
        subjects[-1]['end_index'] = len(webContent)
    answers = []
    users = []
    date = []
    time = []
    # tree = html.fromstring(text)
    # answer = tree.xpath('//blockquote/text()')
    for subject in subjects:
        text = webContent[subject['start_index']:subject['end_index']]
        start = text.find('<blockquote class="postcontent restore ">')
        end = text.find('</blockquote>')
        message = text[start + len('<blockquote class="postcontent restore ">')+2:end].strip()
        quotation_tag_start = message.find('<div class="bbcode_container">')
        if quotation_tag_start != -1:
            message = message[message.rfind('</div>')+len('</div>'):]
        answers.append(message)
        t1 = text.find('<span class="date">') + len('<span class="date">')
        t2 = text.find('&nbsp;',t1)
        t3 = text.find('<span class="time">', t2) + len('<span class="time">')
        t4 = text.find('</span>', t3)
        t5 = text.find('<span class="memname">', t4) + len('<span class="memname">')
        t6 = text.find('</span>', t5)
        if t5 < t4:
            t5 = text.find('<span class="username guest">', t4) + len('<span class="username guest">')
            t6 = text.find('</span>', t5)
        date.append(text[t1:t2])
        time.append(text[t3:t4])
        users.append(text[t5:t6])
    for idx, val in enumerate(answers):
        subjects[idx]['answer'] = val
        subjects[idx]['users'] = users[idx]
        subjects[idx]['date'] = date[idx]
        subjects[idx]['time'] = time[idx]
    return subjects


def split_subjects_xpath(webpage_url):
    try:
        tree = lxml.html.parse(webpage_url)
        xpatheval = etree.XPathDocumentEvaluator(tree)
    except:
        print('ERROR!')
        print   webpage_url
        return
    user_names = xpatheval('//span[@class="memname"]/text()')
    answers = xpatheval('//span[@class="memname"]/text()')
    date = xpatheval('//span[@class="date"]/text()')
    time = xpatheval('//span[@class="memname"]/text()')

    for idx, val in enumerate(answers):
        subjects[idx]['answer'] = val
        subjects[idx]['users'] = users[idx]
        subjects[idx]['date'] = date[idx]
        subjects[idx]['time'] = time[idx]
    return subjects

def get_topics(url):
    webContent = requests.get(url).text
    topics = []
    pattern = re.compile('<h5 class="forumtitle">')
    for m in pattern.finditer(webContent):
        t1 = len('<a href="') + webContent.find('<a href="', m.start())
        t2 = webContent.find('&', t1)
        t3 = webContent.find('>', t2)
        t4 = webContent.find('<', t3)
        t5 = len('Tematy:') + webContent.find('Tematy:', t4)
        t6 = webContent.find('<', t5)
        t7 = len('Posty:') + webContent.find('Posty:', t6)
        t8 = webContent.find('<', t7)
        topics.append({'webpage': 'url', 'start_index': m.start(), 'href': webContent[t1:t2],
                       'title': webContent[t3+1:t4], 'subjects_num': webContent[t5:t6].strip().replace('.', ''),
                       'posts_num': webContent[t7:t8].strip().replace('.', '')})
    return topics


def get_threads(url):
    tree = lxml.html.parse(url)
    xpatheval = etree.XPathDocumentEvaluator(tree)
    web_pages_num_xpath = xpatheval('//a[@class="popupctrl" and contains(text(),"Strona 1 z")]/text()')
    if len(web_pages_num_xpath) == 0:
        threads_web_pages = 1
    else:
        t1 =  len('Strona 1 z ')
        threads_web_pages = int(web_pages_num_xpath[0][t1:].strip())
    topics = []
    for x in range(1, threads_web_pages + 1):
        tree = lxml.html.parse(url+'/page'+str(x))
        xpatheval = etree.XPathDocumentEvaluator(tree)
        titles = xpatheval("//a[contains(@class,'title') and not( contains(@href,'http'))]/text()")
        hrefs = xpatheval("//a[contains(@class,'title') and not( contains(@href,'http'))]/@href")
        assert len(titles) == len(hrefs)
        for idx, m in enumerate(titles):
            topics.append({'href': hrefs[idx], 'title': m})
    print('loading thread from '+ url +' done. ')
    return {v['href']: v for v in topics}.values()
