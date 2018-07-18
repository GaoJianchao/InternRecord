#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 19:18
# @Author  : zql
# @Site    :
# @Version : 3.6
# @File    : dakgja.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

browser = webdriver.PhantomJS()
browser.get('https://nba.hupu.com/stats/teams')
html = browser.page_source
soup = bs(html, 'lxml')
table = soup.find('table')
f = open('score.nba.team.txt', 'w', encoding='utf-8')
count = 0
for tr in table.findAll('tr'):
    if count < 2:
        count += 1
        continue
    for td in tr.findAll('td'):
        f.write(td.getText()+'\t')
        print(td.getText())
    f.write('\n')
    print
f.close()
browser.close()

# import requests
# from bs4 import BeautifulSoup as bs
# from selenium import webdriver
#
# browser = webdriver.Chrome()
# browser.get('https://nba.hupu.com/stats/players')
# html = browser.page_source
# soup = bs(html, 'lxml')
# table = soup.find('table')
# f = open('score.nba.txt', 'w', encoding='utf-8')
# for tr in table.findAll('tr'):
#     for td in tr.findAll('td'):
#         f.write(td.getText()+'\t')
#         print(td.getText())
#     f.write('\n')
#     print
# f.close()