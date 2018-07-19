# QQ音乐爬虫

    在该项目中，通过给定的歌手列表，对该歌手的歌曲进行爬取。

## 目录

1. 爬取qq音乐，对特定的URL发送精心构造的请求，获得某歌手的歌曲，qq-music-scrapy项目利用scrapy框架+python3.6，获取每个指定歌手的大部分歌曲，同时将获取的歌曲按照一定的格式写入文件

2. qq-music-singer-hot-song项目也是利用scrapy框架+python2.7，对指定歌手，只爬取近期热门歌曲[热门歌曲是该歌手页面排行Top歌曲]

### 执行方式

    可以导入pycharm中，直接运行entrypoint.py文件，或者是在当前目录下命令行界面中直接python entrypoint.py的方式运行项目

### 第三方库

---

- fake-useagent
- selenium