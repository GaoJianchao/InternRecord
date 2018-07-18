#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 16:18
# @Author  : zql
# @Site    :
# @Version : 3.6
# @File    : CBA_Spyder.py
# @Software: PyCharm
import requests
user_agent = 'User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)'
headers = {'User-Agent': user_agent}
url = 'http://china.nba.com/static/data/league/playerlist.json'
# 解析网页
r = requests.get(url, headers=headers).json()
num = int(len(r['payload']['players']))-1  # 得到列表r['payload']['players']的长度
p1_cols = []  # 用来存放p1数组的列
p2_cols = []  # 用来存放p2数组的列
# 遍历其中一个['playerProfile']，['teamProfile'] 得到各自列名，添加到p1_cols和p2_cols列表中
detail = r['payload']['players']
f = open('nba.information', 'w', encoding='utf-8')
for i in range(num+1):
    player_data = detail[i]['playerProfile']
    player_name = player_data['displayName']
    player_country = player_data['country']
    player_position = player_data['position']
    team = detail[i]['teamProfile']['name']
    f.write(player_name+'\t'+team+'\t'+player_position+'\t'+player_country+'\n')
f.close()
