# imports
import random
import os
import json
import shutil
from urllib.parse import urlparse

import requests
import sumy
from bs4 import BeautifulSoup

from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.parsers.plaintext import PlaintextParser #We're choosing a plaintext parser here, other parsers available for HTML etc.
from sumy.nlp.tokenizers import Tokenizer



def summarize_text(text, n_sentences):
    '''takes text and summarizes it using sumy and textrank'''
    summarizer = TextRankSummarizer()
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summary = summarizer(parser.document, sentences_count=n_sentences) #Summarize the document with 5 sentences
    summ =' '
    for sentence in summary:
        summ += str(sentence) + ' '
    return summ


def get_hours():
    try:
        url = 'https://api3.libcal.com/api_hours_today.php?iid=1433&lid=0&format=json&systemTime=0'
        r = requests.get(url)
        hours = r.json()

    except:
        hours = json.load(open(app.static_url_path + '/cached_hours.json'))
    parsed = [(l['name'], l['rendered'])
               for l in hours['locations'] if l['name'] != 'Museum']
    return parsed


def get_book():
    try:
        url = 'https://lgapi-us.libapps.com/widgets.php?site_id=538&widget_type=8&output_format=1&widget_embed_type=2&guide_id=731798&box_id=16491701&map_id=19425291&content_only=0&config_id=1540829037986'
        r = requests.get(url)
        
        soup = BeautifulSoup(r.text, 'lxml')
        books = soup.find_all('ul', {'class' : 's-lg-link-list'})[0].find_all('li')
        b = random.choice(books)
        book = {}
        book['title'] = b.find_all(
            'span', {'class': 's-lg-book-title'})[0].text.strip()
        book['image'] = 'https:' + b.findAll('img')[0]['src']
        book['call_number'] = b.find_all(
            'div', {'class': 's-lg-book-prop-callno'})[0].text.strip()
        # AUTOMATICALLY SUMMARIZE TEXT
        book['description'] = summarize_text(b.find_all(
            'div', {'class': 's-lg-link-desc'})[0].text.strip(), n_sentences=3)

        return book
    except:
        print('book error')
        pass



def get_announcement():
    try:
        url = 'https://lgapi-us.libapps.com/widgets.php?site_id=538&widget_type=8&output_format=1&widget_embed_type=2&guide_id=731798&box_id=16573978&map_id=19520868&content_only=0&config_id=1516300042210'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        announcements = soup.findAll(
            "div", {"class": 's-lib-box-content'})[0].find_all('div')
        return random.choice(announcements)
    except:
        print('announcement error')
        pass

#
# def get_database():
#     url = 'https://lgapi-us.libapps.com/widgets.php?site_id=538&widget_type=8&output_format=1&widget_embed_type=2&guide_id=731798&box_id=17105918&map_id=20134804&content_only=0&config_id=1516382018823'
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'lxml')
#     database = soup.findAll(
#         "div", {"class": 's-lib-box-content'})[0].find_all('div')
#     return random.choice(database)

def get_database():
    try:
        url = 'https://lgapi-us.libapps.com/widgets.php?site_id=538&widget_type=8&output_format=1&widget_embed_type=2&guide_id=731798&box_id=18109404&map_id=21277695&content_only=0&config_id=1517875561340'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        dbs = soup.find_all('div', {'class' : 's-lib-box-content'})[0].find_all("div", id=lambda value: value and value.startswith("s-lg-content"))
        d = random.choice(dbs)
        db = {}
        db['title'] = d.find_all('h3')[0].text.strip()
        db['image'] =  d.findAll('img')[0]['src']
        # db['description'] = str(d.findAll('ul', {'id' : 'database-bullets'})[0])
        db['description'] = d.findAll('div', {'id' : 'database-description'})[0].text.strip()
        return db

    except:
        pass
#
#
# def get_database2():
#     try:
#         url = 'https://lgapi-us.libapps.com/widgets.php?site_id=538&widget_type=8&output_format=1&widget_embed_type=2&guide_id=731798&box_id=17753397&map_id=20868259&content_only=0&config_id=1516388024201'
#         r = requests.get(url)
#         soup = BeautifulSoup(r.text, 'lxml')
#         dbs = soup.find_all('ul', {'class' : 's-lg-link-list'})[0].find_all('li')
#         d = random.choice(dbs)
#         db = {}
#         db['title'] = d.find_all('a')[0].text.strip()
#         db['image'] =  d.findAll('img')[0]['src']
#         db['description'] = d.findAll('div', {'class' : 's-lg-database-desc'})[0].text.strip()
#         return db
#     except:
#         pass






def get_message(libraryname):
    try:
        url = 'https://spreadsheets.google.com/feeds/list/18Oe0P9tO_j3z8sh1Z5hcsOmk4S4aPXRRPK3j_DcvPBQ/1/public/values?alt=json'
        r = requests.get(url)
        data = r.json()
    except:
        data = json.load(open('static/cached_messages.json'))
        print(data)
    messages = data['feed']['entry']
    dc_msgs, hb_msgs, gen_msgs = [], [], []
    for m in messages:
        dc_msgs.append(m.get('gsx$downcity')['$t'])
        hb_msgs.append(m.get('gsx$harborside')['$t'])
        gen_msgs.append(m.get('gsx$general')['$t'])
    if libraryname == 'harborside':
        out = hb_msgs + gen_msgs
    elif libraryname == 'all':
        out = hb_msgs + dc_msgs + gen_msgs
    elif libraryname == 'downcity':
        out = dc_msgs + gen_msgs
    else:
        out = gen_msgs
    out = [m for m in out if m != '']
    return {'messages': out}



# def get_poster():
#     posters = os.listdir('app/static/posters')
#     return random.choice(posters)


def get_poster():
    try:
        url = 'https://lgapi-us.libapps.com/widgets.php?site_id=538&widget_type=8&output_format=1&widget_embed_type=2&guide_id=731798&box_id=20141946&map_id=23640032&content_only=0&config_id=1539613012635'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        imgs = soup.find_all('img')
        img_src = random.choice(imgs)['src']
        # for i in imgs:
        #     store_posters(i['src'])
        return img_src
    except:
        print('poster error')
        pass

def get_poster2():
    try:
        url = 'https://lgapi-us.libapps.com/widgets.php?site_id=538&widget_type=8&output_format=1&widget_embed_type=2&guide_id=731798&box_id=18513023&map_id=21741721&content_only=0&config_id=1520542362937'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        imgs = soup.find_all('img')
        img_src = random.choice(imgs)['src']
        # for i in imgs:
        #     store_posters(i['src'])
        return img_src
    except:
        print('poster error')
        pass




def get_video():
    try:
        url = 'https://lgapi-us.libapps.com/widgets.php?site_id=538&widget_type=8&output_format=1&widget_embed_type=2&guide_id=731798&box_id=20529986&map_id=24089759&content_only=0&config_id=1544210807272'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        vids = soup.find_all('iframe')
        iframe_src = random.choice(vids)
        return iframe_src
    except:
        print('video error')
        pass


def store_posters(img_src):
    img_src = 'https:'+img_src
    path = 'app/cached/' + urlparse(img_src).path.split('/')[-1]
    r = requests.get(img_src, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)



# MODULES TO add


# def get_faq():
'''
Gets faqs tagged with "for_display" or something similar
'''
