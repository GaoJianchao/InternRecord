#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 20:00
# @Author  : zql
# @Site    :
# @Version : 3.6
# @File    : get_football_score.py
# @Software: PyCharm
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver

def get_all_team_infor():
    browser = webdriver.PhantomJS()
    browser.get('https://soccer.hupu.com/g/players/')
    html = browser.page_source
    soup = bs(html, 'lxml')
    table = soup.findAll('div', {'class': 'site_right'})
    #  得到所有的队名和链接
    team_infor = dict()
    for tab in table:
        for one in tab.find_all('a'):
            team_infor[one.text] = one['href']
            print(one['href'])
    return team_infor

def get_detail_infor(url):
    infor = requests.get(url)
    soup = bs(infor.content, 'lxml')
    table = soup.findAll('div', {'class': 'player_bg'})
    result_list = list()
    for tab in table:
        if tab != None:
            try:
                people = list()
                player_info = tab.div.ul.children
                for ch in player_info:
                    name = ch.find('a')
                    if name != -1 and name != None:
                        print(name.text)
                        people.append(name.text)
                    rate = ch.find('span')
                    if rate != -1 and rate != None:
                        if rate.text == '暂无评分':
                            print(str(0))
                            people.append(str(0))
                        else:
                            print(rate.text)
                            people.append(rate.text)
                player_margin = tab.find('div', {'class': 'player_margin'})
                tag = player_margin.ul
                center = tag.find('li', {'class': 'center'})
                c_text = center.text
                ind1 = c_text.find('俱乐部:')
                jiancheng = c_text[:ind1].split(":")[1]
                print(jiancheng.strip())
                people.append(jiancheng.strip())
                ind2 = c_text.find('俱乐部号码:')
                clud = c_text[ind1:ind2].split(":")[1]
                print(clud.strip())
                people.append(clud.strip())
                right = tag.find('li', {'class': 'right'})
                r_text = right.text
                ind3 = r_text.find('国籍:')
                position = r_text[:ind3].split(":")[1]
                print(position.strip())
                people.append(position.strip())
                ind4 = r_text.find('年龄:')
                nation = r_text[ind3:ind4].split(":")[1]
                print(nation.strip())
                people.append(nation.strip())
                result_list.append(people)
            except:
                pass
    return result_list

def save_to_txt(key, result_list, f):
    for li in result_list:
        f.write(key + '\t' + '\t'.join(li) + '\n')
    f.flush()

if __name__ == '__main__':
    team_infor = get_all_team_infor()
    f = open('result.txt', 'w', encoding='utf-8')
    for key in team_infor:
        result_list = get_detail_infor(team_infor[key])
        save_to_txt(key, result_list,f)
    f.close()
