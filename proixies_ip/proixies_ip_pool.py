#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/11 17:22
# @Author  : zql
# @Site    :
# @Version : 2.7
# @File    : proixies_ip_pool.py
# @Software: PyCharm
from fake_useragent import UserAgent
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from lxml import etree
import re
from multiprocessing import Process, Queue
import random


class ProixyIP:

    ua = UserAgent()
    protocol = 'http://'  #  仅设定为http代理，可扩展为https
    proxies = list()  # 存储爬取并验证后的代理ip

    def __init__(self, page=3, filename='all.proxies.txt'):
        self.filename = filename
        self.page = page
        self.get_xicidaili_proxies()
        self.get_kuaidaili_proxies()
        # self.get_data5u_proxies()
        # self.get_66ip_proxies()
        self.get_guobanjia_proxies()
        self.get_mimiip_proxies()
        # self.get_ip3366_proxies()
        # self.get_iphai_proxies()
        # self.get_jiangxianli_proxies()
        # self.get_gatherproxy_proxies()
        # self.get_proxylistplus_proxies()
        # self.get_coderbusy_proxies()
        # self.get_cn_proxy_proxies()
        print(len(self.proxies))
        self.verify_proxies()

    '''
    page: 爬取的页数
    write_tag:是否写入文件
    '''
    def get_init(self, page=3):
        self.page = page
        self.get_xicidaili_proxies()
        self.get_kuaidaili_proxies()
        # self.get_data5u_proxies()
        # self.get_66ip_proxies()
        self.get_guobanjia_proxies()
        self.get_mimiip_proxies()
        # self.get_ip3366_proxies()
        # self.get_iphai_proxies()
        # self.get_jiangxianli_proxies()
        # self.get_gatherproxy_proxies()
        # self.get_proxylistplus_proxies()
        # self.get_coderbusy_proxies()
        # self.get_cn_proxy_proxies()
        self.verify_proxies()

    def write_all_proxies(self):
        f = open(self.filename, 'w')
        for item in self.proxies:
            f.write(item+'\n')
        f.close()

    def get_all_proixy(self):
        return self.proxies

    def get_headers(self):
        s_line = self.ua.random
        headers = {'User-Agent': s_line}
        return headers

    def get_xicidaili_proxies(self):
        page = 1
        page_stop = page + self.page
        print('start to get xicidaili ip...')
        while page < page_stop:
            url = 'http://www.xicidaili.com/nt/%d' % page
            html = requests.get(url, headers=self.get_headers()).content
            soup = bs(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def get_kuaidaili_proxies(self):
        print('start to get kuaidaili ip...')
        url_list = ['https://www.kuaidaili.com/free/inha/{page}/',
            'https://www.kuaidaili.com/free/intr/{page}/']
        for url in url_list:
            for page in range(1, self.page):
                page_url = url.format(page=page)
                html = requests.get(page_url, headers=self.get_headers()).content
                tree = etree.HTML(html)
                proxy_list = tree.xpath('.//table//tr')
                for tr in proxy_list[1:]:
                    protocol = tr.xpath('./td/text()')[3].lower() + '://'
                    self.proxies.append(protocol + ':'.join(tr.xpath('./td/text()')[0:2]))

    def get_data5u_proxies(self):
        print('start to get data5u ip...')
        url_list = [
            'http://www.data5u.com/',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml'
        ]
        for url in url_list:
            html = requests.get(url, headers=self.get_headers()).content
            html_tree = etree.HTML(html)
            ul_list = html_tree.xpath('//ul[@class="l2"]')
            for ul in ul_list:
                try:
                    self.proxies.append(self.protocol + ':'.join(ul.xpath('.//li/text()')[0:2]))
                except Exception as e:
                    print(e)

    def get_66ip_proxies(self, area=33, page=3):
        try:
            print('start to get 66ip ip...')
            area = 33 if area > 33 else area
            for area_index in range(1, area + 1):
                for i in range(1, page + 1):
                    url = "http://www.66ip.cn/areaindex_{}/{}.html".format(area_index, i)
                    html = requests.get(url, headers=self.get_headers(), timeout=20).content
                    html_tree = etree.HTML(html)
                    tr_list = html_tree.xpath("//*[@id='footer']/div/table/tr[position()>1]")
                    if len(tr_list) == 0:
                        continue
                    for tr in tr_list:
                        self.proxies.append(
                            self.protocol + tr.xpath("./td[1]/text()")[0] + ":" + tr.xpath("./td[2]/text()")[0])
                    break
        except Exception as e:
            print e

    def get_guobanjia_proxies(self):
        print('start to get goubanjia ip...')
        url = "http://www.goubanjia.com/"
        html = requests.get(url, headers=self.get_headers()).content
        tree = etree.HTML(html)
        proxy_list = tree.xpath('//td[@class="ip"]')
        # 此网站有隐藏的数字干扰，或抓取到多余的数字或.符号
        # 需要过滤掉<p style="display:none;">的内容
        xpath_str = """.//*[not(contains(@style, 'display: none'))
                                        and not(contains(@style, 'display:none'))
                                        and not(contains(@class, 'port'))
                                        ]/text()
                                """
        for each_proxy in proxy_list:
            try:
                # :符号裸放在td下，其他放在div span p中，先分割找出ip，再找port
                ip_addr = ''.join(each_proxy.xpath(xpath_str))
                port = each_proxy.xpath(".//span[contains(@class, 'port')]/text()")[0]
                self.proxies.append(self.protocol + '{}:{}'.format(ip_addr, port))
            except Exception as e:
                pass

    def get_mimiip_proxies(self):
        url_gngao = ['http://www.mimiip.com/gngao/%s' % n for n in range(1, 10)]  # 国内高匿
        url_gnpu = ['http://www.mimiip.com/gnpu/%s' % n for n in range(1, 10)]  # 国内普匿
        url_gntou = ['http://www.mimiip.com/gntou/%s' % n for n in range(1, 10)]  # 国内透明
        url_list = url_gngao + url_gnpu + url_gntou
        print('start to get mimiip ip...')
        for url in url_list:
            r = requests.get(url)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W].*<td>(\d+)</td>', r.text)
            for proxy in proxies:
                self.proxies.append(self.protocol + ':'.join(proxy))

    def get_ip3366_proxies(self):
        print('start to get ip3366 ip...')
        url = 'http://www.ip3366.net/free/'
        r = requests.get(url)
        proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
        for proxy in proxies:
            self.proxies.append(self.protocol + ":".join(proxy))

    def get_iphai_proxies(self):
        """
        IP海 http://www.iphai.com/free/ng
        :return:
        """
        print('start to get iphai ip...')
        urls = [
            'http://www.iphai.com/free/ng',
            'http://www.iphai.com/free/np',
            'http://www.iphai.com/free/wg',
            'http://www.iphai.com/free/wp'
        ]
        for url in urls:
            r = requests.get(url)
            proxies = re.findall(r'<td>\s*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*?</td>[\s\S]*?<td>\s*?(\d+)\s*?</td>',
                                 r.text)
            for proxy in proxies:
                self.proxies.append(self.protocol + ":".join(proxy))

    def get_jiangxianli_proxies(self, page_count=8):  # guobanjia http://ip.jiangxianli.com/?page=

        print('start to get jiangxianli ip...')
        for i in range(1, page_count + 1):
            url = 'http://ip.jiangxianli.com/?page={}'.format(i)
            html = requests.get(url, headers=self.get_headers()).content
            html_tree = etree.HTML(html)
            tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
            if len(tr_list) == 0:
                continue
            for tr in tr_list:
                self.proxies.append(self.protocol + tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0])

    def get_gatherproxy_proxies(self):  #  爬取gatherproxy,墙外的网站
        print('start to get gatherproxy ip...')
        url_list = list()
        url_list.append('http://www.gatherproxy.com/zh/proxylist/anonymity/?t=Anonymous')  # 高匿
        url_list.append('http://www.gatherproxy.com/zh/proxylist/anonymity/?t=Transparent')  # 透明
        url_list.append('http://www.gatherproxy.com/zh/proxylist/anonymity/?t=Elite')  # 原始
        for url in url_list:
            browser = webdriver.PhantomJS()
            browser.get(url)
            html = browser.page_source
            soup = bs(html, 'lxml')
            item = soup.find('table', {'id': 'tblproxy'})
            tag = 1
            for tab in item.find_all('tr'):
                if tag < 3:  #  过滤掉前三行
                    tag += 1
                    continue
                protocol = 'http://'
                self.proxies.append(protocol + ':'.join([x.text for x in tab.find_all('td')[1:3]]))
        browser.quit()

    def get_proxylistplus_proxies(self):  # 墙外的代理
        print('start to get proxylistplus ip...')
        url = 'https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1'
        r = requests.get(url)
        proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
        for proxy in proxies:
            self.proxies.append(self.protocol + ':'.join(proxy))

    def get_coderbusy_proxies(self):  # 码农代理 https://proxy.coderbusy.com/
        try:  # 经常宕机，访问不稳定
            print('start to get coderbusy ip...')
            url = 'https://proxy.coderbusy.com/classical/country/cn.aspx?page=1'
            r = requests.get(url)
            proxies = re.findall('data-ip="(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})".+?>(\d+)</td>', r.text)
            protocol = 'http://'
            for proxy in proxies:
                self.proxies.append(self.protocol + ':'.join(proxy))
        except Exception as e:
            print e
            return

    def get_cn_proxy_proxies(self):  # 墙外网站 cn-proxy
        try:
            print('start to get cn-proxy ip...')
            urls = 'http://cn-proxy.com/archives/218'
            r = requests.get(urls)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\w\W]<td>(\d+)</td>', r.text)
            for proxy in proxies:
                self.proxies.append(self.protocol + ':'.join(proxy))
        except Exception as e:
            print e
            return

    '''
     多进程验证爬取的ip是否有效
     '''

    def verify_proxies(self):
        # 没验证的代理
        old_queue = Queue()
        # 验证后的代理
        new_queue = Queue()
        print ('verify proxy........')
        works = []
        for _ in range(15):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue, new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print ('verify_proxies done!')

    '''
    代理ip的验证：请求百度主页，根据返回的状态码进行判定
    '''
    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0: break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                if requests.get('http://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:
                    print ('success %s' % proxy)
                    if protocol == 'http':
                        new_queue.put(proxy)
            except:
                print ('fail %s' % proxy)

    def verify_ip(self, pro, proxies_list=list()):
        proxies = {'http': pro}
        try:
            if requests.get('http://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:
                print ('success %s' % pro)
                return True
        except:
            print ('fail %s' % pro)
            proxies_list.pop(proxies_list.index(pro))
            return False

    '''
    调用该方法，可以返回一个有效的ip
    当有效ip少于指定数量,会进行重新初始化进行爬取
    保证在proixies中有足够的有效ip
    '''
    def api(self):
        if len(self.proxies) < 3:
            self.get_init()
        tag = False
        while not tag:
            print(len(self.proxies))
            pro = random.choice(self.proxies)
            tag = self.verify_ip(pro, self.proxies)
        proxies = {'http': str(pro)}
        return proxies

if __name__ == '__main__':
    proixy = ProixyIP()
    print(len(proixy.proxies))
    proixy.write_all_proxies()
    print(proixy.api())