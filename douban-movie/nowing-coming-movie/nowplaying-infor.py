# -*- coding: utf-8 -*-
# @Time    : 2018/5/31 20:16
# @Author  : zql
# @Site    :
# @Version : 2.7
# @File    : dingdian.py
# @Software: PyCharm
from bs4 import BeautifulSoup as bs
import time
import requests
from fake_useragent import UserAgent
from selenium import webdriver
import random
from proixies_ip_pool import ProixyIP


class MySpider():

    def __init__(self):
        self.url_list = self.infor_list('now-playing.movie')
        self.f = open('all.now.movie.txt', 'w')

    @staticmethod
    def infor_list(filename):
        infor_list = []
        for line in open(filename):
            arrs = line.strip().split('\t')
            title = arrs[0]
            url = arrs[1]
            infor_list.append([title, str(url)])
        return infor_list

    def start_requests(self, proixy):
        ua = UserAgent()
        for i in range(len(self.url_list)):#
            proxies = proixy.api()
            url = 'https://movie.douban.com/subject/' + str(self.url_list[i][1]) + '/'
            title = self.url_list[i][0]
            content = ua.random
            print(content)
            headers={"User-Agent":ua.random}
            response = requests.get(url,headers=headers, proxies=proxies)
            self.parse(response, title)

    def parse(self, response, title):
        print(response.status_code)
        if response.status_code == 200:
            tmp = bs(response.text, 'lxml')
            try:
                time.sleep(random.randint(1,5))
                tmp_info = tmp.body.find('div', id='info')
                self.save_information(tmp_info, tmp, self.f, title.decode('utf-8'))
            except Exception as e:
                print("ERROR" + e)
                exit(-1)
        else:
            print(response.status_code)

    def save_information(self, tmp_info, tmp, f, title):
        directors = []
        try:
            tag = tmp_info.find_all('a',attrs={'rel':'v:directedBy'})
            if len(tag)==0:
                directors.append("null")
            else:
                for pl in tag:
                    directors.append(pl.text)
        except:
            directors.append("null")
        # 提取主演信息
        cast = []
        try:
            tag = tmp_info.find_all('a',attrs={'rel':'v:starring'})
            if len(tag)==0:
                cast.append("null")
            else:
                for ac in tag:
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
        f.write(title.strip().encode('utf-8','ignore')+'\t')
        for di in range(len(directors)):
            if di!=len(directors)-1:
                f.write(directors[di].strip().encode('utf-8','ignore')+'/')
            else:
                f.write(directors[di].strip().encode('utf-8','ignore')+'\t')
        for ca in range(len(cast)):
            if ca!=len(cast)-1:
                f.write(cast[ca].strip().encode('utf-8','ignore')+'/')
            else:
                f.write(cast[ca].strip().encode('utf-8','ignore')+'\t')
        if flag == 0:# 无异常发生啥时
            for te in range(len(genre)):
                if te!=len(genre)-1:
                    f.write(genre[te].text.strip().encode('utf-8','ignore')+'/')
                else:
                    f.write(genre[te].text.strip().encode('utf-8','ignore')+'\t')
        else:
            f.write("null"+'\t')
        f.write(country.strip().encode('utf-8','ignore')+'\t')
        f.write(release[:10].strip().encode('utf-8','ignore')+'\t')
        alias = alias.split('/')
        for al in range(len(alias)):
            if al!=len(alias)-1:
                f.write(alias[al].strip().encode('utf-8','ignore')+'/')
            else:
                f.write(alias[al].strip().encode('utf-8','ignore')+'\t')
        #提取评分
        try:
            rate = tmp.find('strong',attrs={'property':'v:average'}).text
        except:
            rate = "null"
        f.write(rate.strip().encode('utf-8','ignore')+'\t')
        f.write(rating_people.strip().encode('utf-8','ignore')+'\n')
        print '%s\t%s'%(title.encode('utf-8','ignore'),country.strip().encode('utf-8','ignore'))
        self.f.flush()

if __name__=='__main__':
    my_spyder = MySpider()
    proixy = ProixyIP()
    my_spyder.start_requests(proixy)