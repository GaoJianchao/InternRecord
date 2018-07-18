# -*- coding: utf-8 -*-
# @Time    : 2018/6/2 15:00
# @Author  : zql
# @Site    : 
# @File    : cookie.py
# @Software: PyCharm
class transCookie:
    def __init__(self, cookie):
        self.cookie = cookie

    def stringToDict(self):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = self.cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

if __name__ == "__main__":
    cookie = r'll="108288"; bid=2NwHpUxRiJA; __utmc=30149280; __utmc=223695111; __yadk_uid=amuGGiy7OaNiadvALOOQ1upaSUmi7hPG; _vwo_uuid_v2=D4472535BA8F19203B56D1AADC8833F62|b35cc118452bc3ec39ef118c3ede9a6c; ct=y; ap=1; ps=y; ue="646184101@qq.com"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.15581; _ga=GA1.2.895599414.1527409845; _gid=GA1.2.1790579979.1527902047; __utmz=30149280.1527915289.9.6.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=30149280.895599414.1527409845.1527920562.1527922929.12; __utmt=1; dbcl2="155819096:r17KJyxD8PM"; ck=AHGV; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1527923038%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=d768704d139629f5.1527409845.11.1527923038.1527920572.; _pk_ses.100001.4cf6=*; __utma=223695111.1992032999.1527409845.1527920562.1527923038.11; __utmb=223695111.0.10.1527923038; __utmz=223695111.1527923038.11.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmb=30149280.3.10.1527922929'
    trans = transCookie(cookie)
    print(trans.stringToDict())