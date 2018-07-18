# -*- coding: utf-8 -*-
# @Version : 2.7
"""
Created on Wed May 23 13:12:05 2018

@author: Administrator
"""

from bs4 import BeautifulSoup as bs
import requests

resp = requests.get('https://movie.douban.com/coming')
html_data = resp.content
html_data = html_data.decode("utf-8","ignore")
#print(html_data)

f = open('coming.movie','w+')

soup = bs(html_data, 'html.parser')
coming_movie = soup.find_all('table',class_='coming_list')
tab = coming_movie[0]
flag = True
for tr in tab.findAll('tr'):
    if flag:
        flag = False
        continue
    tag = 1
    for td in tr.findAll('td'):
        f.write(td.getText().strip().encode('utf-8','ignore')+"\t")
        if tag ==2:
            a = td.find('a')
            f.write(a.get('href').strip().encode('utf-8','ignore')+'\t')
            print(a.get('href'))
        tag += 1
    f.write('\n')
f.close()

