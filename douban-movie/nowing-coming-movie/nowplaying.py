# -*- coding: utf-8 -*-
# @Version : 2.7
"""
Created on Wed May 23 12:53:47 2018

@author: Administrator
"""

import requests
resp = requests.get('https://movie.douban.com/nowplaying/beijing/')
html_data = resp.content
html_data = html_data.decode("utf-8","ignore")
from bs4 import BeautifulSoup as bs
soup = bs(html_data, 'html.parser')
nowplaying_movie = soup.find_all('div', id='nowplaying')
nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')

f = open('now-playing.movie','w+')
nowplaying_list = []
for item in nowplaying_movie_list:
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    for tag_img_item in item.find_all('img'):
        f.write(tag_img_item['alt'].encode('utf-8','ignore')+'\t')
        f.write(item['data-subject'] + '\n')
        nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)
        nowplaying_dict['id'] = item['data-subject']
f.close()
