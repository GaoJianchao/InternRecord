# -*- coding: utf-8 -*-
# @Time    : 2018/5/31 20:10
# @Author  : zql
# @Site    : 
# @File    : entrypoint.py
# @Software: PyCharm
from scrapy.cmdline import execute
# from proixies_ip_pool import ProixyIP
# pro = ProixyIP().write_all_proxies()
execute(['scrapy', 'crawl', 'music'])
