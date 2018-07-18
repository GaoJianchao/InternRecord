# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from fake_useragent import UserAgent
from proixies_ip_pool import ProixyIP


# 仿照scrapy内置的UserAgentMiddleware，来自定义设置user-agent的中间件。
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

    def __init__(self):
        self.proxies = open('all.proxies.txt').readlines()

    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        print("**************ProxyMiddleware no pass************" + proxy)
        request.meta['proxy'] = proxy
