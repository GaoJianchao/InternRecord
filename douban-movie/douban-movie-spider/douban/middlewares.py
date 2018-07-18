# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import base64
from fake_useragent import UserAgent
from urllib import request
import random

""" 阿布云ip代理配置，包括账号密码 """
proxyServer = "http://http-cla.abuyun.com:9030"
proxyUser = "H90AR3769461565C"
proxyPass = "010EA78AA249911A"
# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")


def linkWithProxy(self, line):
    lineList = line.split('\t')
    protocol = lineList[3].lower()
    server = protocol + r'://' + lineList[1] + ':' + lineList[2]
    opener = request.build_opener(request.ProxyHandler({protocol: server}))
    request.install_opener(opener)
    try:
        response = request.urlopen('http://www.baidu.com/', timeout=3)
    except:
        print('%s connect failed!\n' % server)
        return False
    else:
        try:
            strRe = response.read()
        except:
            print('%s connect failed!\n' % server)
            return False
        if self.regex.search(str(strRe)):
            print('%s connect success!！！！！！！\n' % server)
            return True


def get_ip():
    with open('alive_ip.txt') as f:
        lines = f.readlines()
        tag = False
        while not tag:
            line = random.choice(lines)
            tag = linkWithProxy(line)
    return line


class ABProxyMiddleware(object):
    """ 阿布云ip代理配置 """
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth


#仿照scrapy内置的UserAgentMiddleware，来自定义设置user-agent的中间件。
class RandomUserAgent(object):
    def __init__(self, crawler):
        super(RandomUserAgent, self).__init__()
        self.ua = UserAgent()
        # 从配置文件settings中读取RANDOM_UA_TYPE值,如果配置不存在，则采用默认的random进行随机。
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')
    # 注意：from_crawler函数名以及参数必须和内置的保持一致

    @classmethod
    def from_crawler(cls, crawler):
        # 在scrapy内置请求头中间件中，该方法的作用是返回了当前类的对象
        return cls(crawler)

    def process_request(self, request, spider):
        # 该方法是处理请求头的核心方法，在该方法内部指定请求头的User_Agent值。
        # request.headers.setdefault(b"User-Agent", random.choice(self.user_agent_list))
        def get_user_agent():
            # 返回的就是最终的User-Agent，类似于对象.属性
            return getattr(self.ua, self.ua_type)
        request.headers.setdefault(b"User-Agent", get_user_agent())


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        line = get_ip()
        proxy = line.strip().split('\t')
        print("**************ProxyMiddleware no pass************" + proxy[0])
        request.meta['proxy'] = proxy[2]+"://%s:%s" % (proxy[0], proxy[1])




