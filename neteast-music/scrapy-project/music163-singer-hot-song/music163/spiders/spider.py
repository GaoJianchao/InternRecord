# -*- coding: utf-8 -*-
# @Version : 2.7
from scrapy import Spider, Request
from bs4 import BeautifulSoup as bs


class MusicSpider(Spider):
    name = "music"
    allowed_domains = ["163.com"]
    base_url = 'https://music.163.com'
    ids = ['1001', '1002', '1003']
    initials = [i for i in range(65, 91)]+[0]

    def __init__(self):
        self.f = open('singer-song-album.txt', 'w')

    def start_requests(self):
        for id in self.ids:
            for initial in self.initials:
                url = '{url}/discover/artist/cat?id={id}&initial={initial}'.format(url=self.base_url, id=id, initial=initial)
                yield Request(url, callback=self.parse_index)

    # 获得所有歌手的url
    def parse_index(self, response):
        # 网易云音乐的歌手页有两个组成部分，上方十个带头像的热门歌手和下方只显示姓名的普通歌手
        for sel in response.xpath('//*[@id="m-artist-box"]/li/*'):
            artist = sel.re('href\=\"\/artist\?id\=[(0-9)]{4,9}')
            for artistid in artist:
                artist_url = self.base_url + artistid[6:]  #
                print(artist_url)
                yield Request(artist_url, callback=self.parse)
                
    # 获得所有歌手专辑的url
    def parse(self, response):
        song_list = list()
        soup = bs(response.body, 'lxml')
        singer = soup.title.text.encode('utf-8')
        singer = singer.split(' ')[0]
        table = soup.find('ul', {'class': 'f-hide'})
        for li in table.find_all('li'):
            song = li.text.encode('utf-8')
            song_list.append(song)
        for item in song_list:
            print(singer + '\t' + item)
            self.f.write(singer + '\t' + item + '\n')
            self.f.flush()
