#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 16:43
# @Author  : zql
# @Site    :
# @Version : 2.7
# @File    : net.py
# @Software: PyCharm
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import random
from multiprocessing import Process, Queue
import os, time, re
from selenium import webdriver
import copy


class NetSpider():

    def __init__(self):
        ua = UserAgent()
        self.base_url = 'https://music.163.com'
        self.ids = ['1001', '1002', '1003']  #
        self.initials = [i for i in range(65, 91)] + [0]  #
        self.verify_pro = list()
        self.artist_id_list = list()
        self.headers = {'User-Agent': ua.random}

    def get_artist_id(self):
        for _id in self.ids:
            for initial in self.initials:
                print(str(_id)+'\t'+str(initial))
                url = '{url}/discover/artist/cat?id={id}&initial={initial}'.format(url=self.base_url,
                                                                                   id=_id, initial=initial)
                html_file = requests.get(url, headers=self.headers)
                print(str(html_file.status_code))
                response = bs(html_file.content, 'lxml')
                for sel in response.xpath('//*[@id="m-artist-box"]/li/*'):
                    artist = sel.re('href\=\"\/artist\?id\=[(0-9)]{4,9}')
                    for artistid in artist:
                        artist_url = self.base_url + artistid[6:]  #
                        print(artist_url)
                        self.artist_id_list.append(artist_url)
                # for sel in response.find('ul', {'id': 'm-artist-box', 'class': 'm-cvrlst m-cvrlst-5 f-cb'}):
                #     ch = sel.find('a')
                #     if type(ch) != int and ch.text.strip()!='':
                #         artist_url = self.base_url + ch['href']  # 跳转每个歌手的热门歌曲页面
                #         self.artist_id_list.append(artist_url)

    def get_song_list(self, url, f):
        bad_url = str()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
        song_list = list()
        html = requests.get(url, headers=self.headers)  # , proxies=proixy
        print(url)
        print(html.status_code)
        time.sleep(1)
        soup = bs(html.content, 'lxml')
        singer = soup.title.text.encode('utf-8')
        singer = singer.split(' ')[0]
        f.write(singer+'\t'+url+'\n')
        try:
            table = soup.find('ul', {'class': 'f-hide'})
            for li in table.find_all('li'):
                song = li.text.encode('utf-8')
                song_list.append(song)
        except:
            try:
                table = soup.find('table', {'class': 'm-table m-table-1 m-table-4'})
                for tr in table.find_all('tr'):
                    td = tr.find_all('td')[1]
                    print(td.find('b')['title'])
                    song_list.append(td.find('b')['title'].encode('utf-8'))
            except Exception as e:
                bad_url = url
                print e
        return [singer, song_list, bad_url]


if __name__ == '__main__':
    fst = open('id_list', 'w')
    fs = open('song.txt', 'w')
    spider = NetSpider()
    spider.get_artist_id()
    id_list = spider.artist_id_list
    for id in id_list:
        [singer, song_list, bad_url] = spider.get_song_list(id, fst)
        for item in song_list:
            print(singer + '\t' + item)
            fs.write(singer + '\t' + item + '\n')
    fs.close()
    fst.close()