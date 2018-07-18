# -*- coding: gbk -*-
# @Version : 3.6
import scrapy
from scrapy import Request
import json
import re
import urllib.parse


class RequestUrlSpider(scrapy.Spider):
    name = "requestUrl"
    allowed_domains = ["www.y.qq.com"]
    start_urls = ['http://www.y.qq.com/']

    url="https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.song&searchid=56365046261055832&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p={page}&n=50&w={singer}&g_tk=5381&jsonpCallback=searchCallbacksong412&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"

    def __init__(self):
        self.singerName = self.get_singer_list()
        self.f = open('song-singer-album.txt', 'a', encoding='gbk', errors='ignore')
        self.singer = ''

    @staticmethod
    def get_singer_list():
        singer_list = []
        with open('singer.txt') as f:
            lines = f.readlines()
            for line in lines:
                singer_list.append(line.strip().split('\t')[0])
        return singer_list

    def start_requests(self):
        for i in range(len(self.singerName)):
            self.singer = self.singerName[i]
            singer = urllib.parse.quote(self.singerName[i])
            for j in range(1, 7):
                yield Request(url=self.url.format(singer=singer, page=str(j)), callback=self.parse)

    @staticmethod
    def dealjson(response, pattern):
        text = response.text
        text = re.sub(pattern[0], '', text)
        text = re.sub(pattern[1], '', text)
        jsondata = json.loads(text)
        return jsondata

    def parse(self, response):
        jsondata = self.dealjson(response, ["^searchCallbacksong\d{0,}\(", "\)$"])
        message = jsondata['message']
        if message == '':
            songdetail = jsondata["data"]["song"]
            length = len(songdetail["list"])
            for i in range(length):
                singer_list = []
                item = songdetail["list"][i]
                album = item["album"]['name']
                album = album.strip()
                if album == '' or album == '空' or album is None:
                    album = 'null'
                song = item['name']
                singer_ = item['singer']
                tag = False
                for it in singer_:
                    if it['name'].strip() != '':
                        singer_list.append(it['name'])
                        if it['name'] in self.singerName:
                            tag = True
                if not tag:
                    continue
                singers = "|".join(singer_list)
                print(singers + '\t' + self.singer)
                if song == '':
                    continue
                print(song + '\t' + singers + '\t' + album)
                self.f.write(song + '\t' + singers + '\t' + album + '\n')
