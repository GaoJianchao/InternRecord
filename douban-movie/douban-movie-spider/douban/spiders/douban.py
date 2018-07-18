# -*- coding: utf-8 -*-
# @Time    : 2018/5/31 20:16
# @Author  : zql
# @Site    :
# @Version : 3.6
# @File    : dingdian.py
# @Software: PyCharm
import scrapy
from bs4 import BeautifulSoup as bs
from scrapy.http import Request
import xlrd
import time
import requests
import urllib


class MySpider(scrapy.Spider):
    name = 'douban'
    allowed_domain = ['movie.douban.com/subject/']

    def __init__(self):
        self.url_list = self.infor_list('movie.xlsx')
        self.f = open('all.movie.txt', 'w', encoding='utf-8')
        # self.cookie = self.login()

    @staticmethod
    def infor_list(filename):
        infor_list = []
        for line in open(filename):
            arrs = line.strip().split('\t')
            title = arrs[1].decode('gbk').encode('utf-8')
            url = arrs[2].decode('gbk').encode('utf-8')
            infor_list.append([title, str(url)])
        return infor_list

    def start_requests(self):
        for i in range(len(self.url_list)):#
            url = str(self.url_list[i][1])
            yield Request(url, self.parse)

    def parse(self, response):
        print(response.status)
        if response.status == 200:
            tmp = bs(response.text, 'lxml')
            try:
                time.sleep(1)
                tmp_info = tmp.body.find('div', id='info')
                self.save_information(tmp_info, tmp, self.f)
            except:  # 被封了
                print("ERROR")
                # self.cookie = self.login()
                print(tmp)
                time.sleep(300)
        else:
            print(response.status)

    def save_information(self, tmp_info, tmp, f):

        # 提取<div id='info'>的部分

        # 提取导演信息
        directors = []
        try:
            for pl in tmp_info.find_all('a', attrs={'rel': 'v:directedBy'}):
                directors.append(pl.text)
        #            print(pl.text)
        except:
            directors.append("null")
        # 提取主演信息
        cast = []
        try:
            for ac in tmp_info.find_all('a', attrs={'rel': 'v:starring'}):
                cast.append(ac.text)
        #            print(ac.text)
        except:
            cast.append("null")
        # 提取类型标签
        flag = 0
        try:
            genre = tmp_info.find_all('span', property='v:genre')
        #        print(genre)
        except:
            flag = 1
            genre = "null"
        # 提取国家,搜索<span>制片国家/地区:</span>的下个兄弟节点
        try:
            country = tmp_info.find('span', text='制片国家/地区:').next_sibling[1:]
        #        print(country)
        except:
            country = 'null'
        # 提取第一个上映日期,搜索<span property='v:initialReleaseDate'></span>中的文本值
        try:
            release = tmp_info.find('span', property='v:initialReleaseDate').text
        #        print(release)
        except:
            release = "null"
        # 提取别名,搜索<span>又名:</span>的下个兄弟节点
        try:
            alias = tmp_info.find('span', text='又名:').next_sibling[1:]
        #        print(alias)
        except:
            alias = "null"
        # 打分人数，搜索<span property='v:votes'>标签中的content属性
        try:
            rating_people = tmp.find('span', property='v:votes').getText()
        #        print(rating_people)
        except:
            rating_people = "null"
        # 电影名称信息
        try:
            title = tmp.find('span', property='v:itemreviewed').getText()
        except:
            title = 'null'
        # 写电影名
        try:
            f.write(title.strip() + '\t')
        except:
            f.write("***" + '\t')
        # 写导演
        for di in range(len(directors)):
            if di != len(directors) - 1:
                try:
                    f.write(directors[di] + '/')
                except:
                    f.write("***" + '/')
            else:
                try:
                    f.write(directors[di] + '\t')
                except:
                    f.write("***" + '\t')
        # 写主演
        for ca in range(len(cast)):
            if ca != len(cast) - 1:
                try:
                    f.write(cast[ca] + '/')
                except:
                    f.write("***" + '/')
            else:
                try:
                    f.write(cast[ca] + '\t')
                except:
                    f.write("***" + '\t')
        if flag == 0:  # 无异常发生啥时
            for te in range(len(genre)):
                if te != len(genre) - 1:
                    try:
                        f.write(genre[te].text + '/')
                    except:
                        f.write("***" + '/')
                else:
                    try:
                        f.write(genre[te].text + '\t')
                    except:
                        f.write("***" + '\t')
        else:
            f.write("null" + '\t')
        try:
            f.write(country.strip() + '\t')
        except:
            f.write("***" + '\t')
        try:
            f.write(release[:10].strip() + '\t')
        except:
            f.write("***" + '\t')
        alias = alias.split('/')
        for al in range(len(alias)):
            if al != len(alias) - 1:
                try:
                    f.write(alias[al] + '/')
                except:
                    f.write("***" + '/')
            else:
                try:
                    f.write(alias[al] + '\t')
                except:
                    f.write("***" + '\t')
        # 提取评分
        try:
            rate = tmp.find('strong', attrs={'property': 'v:average'}).text
        #        print(rate)
        except:
            rate = "null"
        try:
            f.write(rate.strip() + '\t')
        except:
            f.write("***" + '\t')
        try:
            f.write(rating_people.strip() + '\n')
        except:
            f.write("***" + '\n')
        print('%s\t%s' % (title, country))
        self.f.flush()

