#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/26 10:09
# @Author  : zql
# @Site    : 
# @File    : get_cba_score.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
import time

def get_team_infor():
    html = requests.get('https://cba.hupu.com/players/')
    html_file = bs(html.content, 'lxml')
    tag = html_file.find('table')
    tag = tag.find('tr',{'style': "color:#333333", "align": "left", "valign": 'top'})
    count = 1
    team_info = dict()
    base_url = 'https://cba.hupu.com/players/'
    for ch in tag.children:
        if count % 2 != 0:
            count += 1
            continue
        for a in ch.find_all('a'):
            team_info[a.text] = str(base_url+a['href'])
            print(a['href']+'\t'+a.text)
        count += 1
    return team_info


def get_deatil_infor(url, browser):
    browser.get(url)
    html = bs(browser.page_source, 'lxml')
    tab = html.find('table')
    result_infor = list()
    for tr in tab.findAll('tr'):
        player_infor = list()
        for td in tr.findAll('td'):
            content = td.text.strip()
            player_infor.append(content)
        result_infor.append(player_infor)
    return result_infor


def save_to_text(result_list, f, key):
    for li in result_list:
        if len(li) == 6 and li[0] != '号码':
            f.write(key + '\t' + '\t'.join(li) + '\n')
    f.flush()


if __name__ == "__main__":
    team_info = get_team_infor()
    f = open('infor_cba.txt', 'w', encoding='utf-8')
    browser = webdriver.PhantomJS()
    for key in team_info:
        result_list = get_deatil_infor(team_info[key], browser)
        save_to_text(result_list, f, key)
    browser.close()

