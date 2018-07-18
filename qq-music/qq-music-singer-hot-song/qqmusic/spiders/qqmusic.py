#!/usr/bin/env python
# -*- coding: gbk -*-
# @Time    : 2018/6/6 18:01
# @Author  : zql
# @Site    :
# @Version : 2.7
# @File    : qqmusic.py
# @Software: PyCharm
import scrapy
from scrapy import Request
import json
import re
import urllib


class GetQQMusic(scrapy.Spider):
    name = "qqmusic"
    allowed_domains = ["www.y.qq.com"]
    start_urls = ['http://www.y.qq.com/']
    url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&" \
          "remoteplace=txt.yqq.center&searchid={mid}&t=0&aggr=1&cr=1&catZhida=1&" \
          "lossless=0&flag_qc=0&p=1&n=20&w={singer}&g_tk=5381&jsonpCallback=MusicJsonCallback{back}" \
          "&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
    singer_list = list()

    def __init__(self):
        self.singer_list = self.getsingerlist()
        self.f = open('singer_song.txt', 'w')

    @staticmethod
    def getsingerlist():
        res = []
        with open('result.txt') as f:
            lines = f.readlines()
            for line in lines:
                res.append(line.strip())
        f.close()
        return res

    @staticmethod
    def dealjson(response, pattern):
        text = response.text
        text = re.sub(pattern[0], '', text)
        text = re.sub(pattern[1], '', text)
        jsondata = json.loads(text)
        return jsondata

    def start_requests(self):
        for i in range(len(self.singer_list)):
            singer = urllib.quote(self.singer_list[i])
            url = self.url.format(singer=singer, mid=str(37197354585475686+i), back=str(9218903382070882))
            yield Request(url, callback=self.parse)

    def parse(self, response):
        jsondata = self.dealjson(response, ["^MusicJsonCallback\d{0,}\(", "\)$"])
        message = jsondata['data']
        if message != '':
            songdetail = jsondata["data"]["song"]
            length = len(songdetail["list"])
            for i in range(length):
                action = songdetail["list"][i]
                album_name = action["album"]['name']
                song = action['title']
                singer = action['singer'][0]['name']
                singers = action['singer']
                name = list()
                for ch in singers:
                    item = ch['name'].encode('utf-8')
                    if item in self.singer_list:
                        name.append(item)
                self.f.write(song.encode('utf-8') + '\t' + '|'.join(name) + '\t' + album_name.encode('utf-8') + '\n')
                print(song.encode('utf-8') + '\t' + singer.encode('utf-8') + '\t' + album_name.encode('utf-8'))
