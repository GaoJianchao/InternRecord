# -*- coding: utf-8 -*-
# @Version : 3.6
from scrapy import Spider, Request


class MusicSpider(Spider):
    name = "music"
    allowed_domains = ["163.com"]
    base_url = 'https://music.163.com'
    ids = ['1001', '1002', '1003', '2001', '2002', '2003', '6001', '6002', '6003', '7001', '7002', '7003', '4001',
           '4002', '4003']
    initials = [i for i in range(65, 91)]+[0]

    def __init__(self):
        self.f = open('singer-song-album.txt', 'w', encoding='gbk', errors='ignore')

    def start_requests(self):
        for id in self.ids:
            print(id)
            self.f.write(str(id)+'\n')
            for initial in self.initials:
                print(initial)
                url = '{url}/discover/artist/cat?id={id}&initial={initial}'.format(url=self.base_url, id=id, initial=initial)
                yield Request(url, callback=self.parse_index)

    # 获得所有歌手的url
    def parse_index(self, response):
        # 网易云音乐的歌手页有两个组成部分，上方十个带头像的热门歌手和下方只显示姓名的普通歌手
        for sel in response.xpath('//*[@id="m-artist-box"]/li/*'):
            artist = sel.re('href\=\"\/artist\?id\=[(0-9)]{4,9}')
            for artistid in artist:
                artist_url = self.base_url + '/artist' + '/album?' + artistid[14:]
                yield Request(artist_url, callback=self.parse_artist_pre)
     
    def parse_artist_pre(self, response):
        # 得到专辑页的翻页html elements列表
        artist_albums = response.xpath('//*[@class="u-page"]/a[@class="zpgi"]/@href').extract()
        if artist_albums == []:   # 若为空，说明只有一页，即套用原parse_artist方法的代码，注意callback=self.parse_album
            albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
            for album in albums:
                album_url = self.base_url + album
                yield Request(album_url, callback=self.parse_album)            
        else:  # 若不为空，即该歌手专辑存在分页，那么得到分页的url，注意callback=self.parse_artist
            for artist_album in artist_albums:
                artist_album_url = self.base_url + artist_album
                yield Request(artist_album_url, callback=self.parse_artist)
                
    # 获得所有歌手专辑的url
    def parse_artist(self, response):
        albums = response.xpath('//*[@id="m-song-module"]/li/div/a[@class="msk"]/@href').extract()
        for album in albums:
            album_url = self.base_url + album
            yield Request(album_url, callback=self.parse_album)

    # 获得所有专辑音乐的url
    def parse_album(self, response):
        musics = response.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        for music in musics:
            music_id = music[9:]
            music_url = self.base_url + music

            yield Request(music_url, meta={'id': music_id}, callback=self.parse)

    # 获得音乐信息
    def parse(self, response):
        music = response.xpath('//div[@class="tit"]/em[@class="f-ff2"]/text()').extract_first()
        artist = response.xpath('//div[@class="cnt"]/p[1]/span/a/text()').extract_first()
        album = response.xpath('//div[@class="cnt"]/p[2]/a/text()').extract_first()
        if artist is not None and music is not None and album is not None:
            self.f.write(artist + '\t' + music + '\t' + album + '\n')
            print(music + '\t' + artist + '\t' + album)
        self.f.flush()

