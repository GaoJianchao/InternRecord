# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from fake_useragent import UserAgent


class RandomUserAgent(object):

    def __init__(self, crawler):
        self.ua = UserAgent()
        # 可读取在settings文件中的配置，来决定开源库ua执行的方法，默认是random，也可是ie、Firefox等等
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    # 更换用户代理逻辑在此方法中
    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
        print(get_ua())
        request.headers.setdefault('User-Agent', get_ua())

