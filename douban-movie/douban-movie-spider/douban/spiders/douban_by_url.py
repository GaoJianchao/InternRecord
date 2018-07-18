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
from urllib.parse import quote
import time
import requests
import urllib


class MySpider(scrapy.Spider):
    name = 'douban_by_url'
    allowed_domain = ['movie.douban.com/subject/']

    def __init__(self):
        self.f = open('url.movie.txt', 'a', encoding='utf-8')
        # self.cookie = self.login()
        self.begin_time = time.time()
        self.urls = 'https://www.douban.com/people/155819096/' # get cookie

    @staticmethod
    def login():
        url = 'http://accounts.douban.com/login'

        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
        }
        data = {
            "redir": "http://movie.douban.com/mine?status=collect",
            "form_email": 'monsterxmonster@163.com',
            "form_password": '18222628410',
            "login": u'zql040694zhang'
        }
        r = requests.post(url, data, headers)

        # 获取验证码图片，并且保存到本地
        soup = bs(r.text, 'lxml')
        imgurl = soup.select('#captcha_image')[0]['src']
        img = urllib.request.urlopen(imgurl).read()
        with open(soup.select('#captcha_image')[0]['src'].split('?')[1][3:7] + '.jpg', 'wb') as f:
            f.write(img)
        # 输入验证码
        code = input("please input the code:")
        data['captcha-solution'] = code
        data['captcha-id'] = soup.select('#captcha_image')[0]['src'].split('?')[1][3:]
        data = urllib.parse.urlencode(data)
        r = requests.post(url, data, headers)
        cookie = r.cookies.get_dict()
        return cookie

    def start_requests(self):
        a = 0
        type_ = '电影'
        while True:
            visit_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=' + quote(type_) + '&start={0}'.format(a*20)
            print(visit_url)
            time.sleep(2)
            a += 1
            yield Request(visit_url, self.parse)#, cookies=self.cookie

    def parse(self, response):
        print(response.status)
        if response.status == 200:
            html_code = eval(response.text)
            print(html_code)
            ll = len(html_code['data'])
            if ll != 0:
                for i in range(ll):
                    dict_ = html_code['data'][i]
                    url_ = dict_['url']
                    print('--------------------------------------')
                    url_ = str(url_).replace('\\', '')
                    print(url_)
                    time.sleep(1)
                    yield Request(url_, self.infor_parser)
            else:
                return
        else:
            print("error...")
            # self.cookie = response.cookies.get_dict()
            time.sleep(120)

    def infor_parser(self, response):
        try:
            tmp = bs(response.text, 'lxml')
            time.sleep(1)
            tmp_info = tmp.body.find('div', id='info')
            self.save_information(tmp_info, tmp, self.f)
        except:  # 被封了
            print("ERROR")
            print(tmp)
            # self.cookie = response.cookies.get_dict()
            time.sleep(120)

    def save_information(self, tmp_info, tmp, f):

        # 提取<div id='info'>的部分

        # 提取导演信息
        directors = []
        try:
            for pl in tmp_info.find_all('a', attrs={'rel': 'v:directedBy'}):
                directors.append(pl.text)
        except:
            directors.append("null")
        # 提取主演信息
        cast = []
        try:
            for ac in tmp_info.find_all('a', attrs={'rel': 'v:starring'}):
                cast.append(ac.text)
        except:
            cast.append("null")
        # 提取类型标签
        flag = 0
        try:
            genre = tmp_info.find_all('span', property='v:genre')
        except:
            flag = 1
            genre = "null"
        # 提取国家,搜索<span>制片国家/地区:</span>的下个兄弟节点
        try:
            country = tmp_info.find('span', text='制片国家/地区:').next_sibling[1:]
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
        except:
            alias = "null"
        # 打分人数，搜索<span property='v:votes'>标签中的content属性
        try:
            rating_people = tmp.find('span', property='v:votes').getText()
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

