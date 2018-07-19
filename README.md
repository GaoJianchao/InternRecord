# InternRecord

## 实习期间看到的、遇到的、学到的东西，进行记录下

## 记录包括：

### 豆瓣电影爬虫

+ douban-movie-spider

  + douban-movie-spider   [python:3.6]

    + douban_by_url

      1. <https://movie.douban.com/j/new_search_subjects?>请求上述网址，每次获取20部电影简要信息以及每部电影的详情url，然后对每部电影逐一解析
      2. 解析的内容包括：
            导演、主演、电影类型、国家、上映日期、别名、打分人数、得分和电影名[注：python2.7版本的format函数可以不用位置标号]
    + douban

      1. 已知每个电影详情界面的url[movie.xlsx文件]，直接通过访问url获取电影的详情信息。
      2. 解析的内容包括：
            导演、主演、电影类型、国家、上映日期、别名、打分人数、得分和电影名

  + nowing-coming-movie  [python:2.7]

    + coming.py: 获取即将上映的电影的概要信息
    + nowplaying.py: 正在热映的电影的概要信息
    + coming-info.py: 即将上映的电影的详细信息
    + nowplaying-infor.py: 正在上映的电影的详细信息
    + 详细信息的解析内容同上

### 网易云音乐爬虫

+ scrapy-project

  + music163-all-singer-album-song    [python:3.6]

    爬取网易云华语、欧美、日本、韩国和其他类别中所有男、女以及组合和乐队的所有专辑的所有歌曲信息
  + music163-singer-hot-song [python:2.7]

    scrapy框架实现的，网易云音乐华语男女歌手以及组合和乐队的热门歌曲信息

+ stan-alone    [python:2.7]

    单线程爬虫：爬取网易云音乐中指定类型的所有歌手，以及他们的热门歌曲,歌手类型代码：

  + 华语：[1001, 1002, 1003]
  + 欧美：[2001, 2002, 2003]
  + 日本：[6001, 6002, 6003]
  + 韩国：[7001, 7002, 7003]
  + 其他：[4001, 4002, 4003]

  爬虫执行流程，以华语男歌手为例：

    获取首页[A开头]的所有歌手信息——>按照页码规则，遍历后续页面——>获得所有的歌手url，存储——>遍历歌手的url——>获取热门歌曲

### qq音乐爬虫

+ qq-music-scrapy

    利用scrapy框架，爬取指定文件中包含的歌手的所有歌曲

    歌手文件：singer.txt    [格式：歌手]    [备注：singer.txt后两列暂时无用]

    爬取结果：result.txt    [格式：歌曲\t歌手\t专辑]

    爬虫运行：python entrypoint.py

    版本：3.6版本

+ qq-music-singer-hot-song

    利用scrapy框架，爬取指定歌手的热门歌曲，整体流程同爬取所有歌手歌曲的流程

    歌手文件：result.txt    [格式：歌手]

    结果文件：singer_song.txt   [格式：歌曲\t歌手\t专辑]

    爬虫运行：python entrypoint.py

    版本：2.7版本

### 虎扑体育爬虫  [python:3.6]

+ get_cba_score

    网址：<https://cba.hupu.com/players/>

    获取CBA球队-序号-球员-身高-体重-位置-出生日期的信息

    例如：广东华南虎	29	李佳益	208CM/6尺10寸	115KG / 253磅	中锋	1997年9月2日

+ NBA_Spyder

    网址：<http://china.nba.com/static/data/league/playerlist.json>

    获取NBA主流球队中球员-球队-位置-国家的信息，

    例如：凯尔 安德森	灰熊	前锋	美国
+ get-football_score

    网址：<https://soccer.hupu.com/g/players/>

    获取国际足球中英超、西甲、意甲、德甲和法甲中球队的球员数据信息

    例如：曼联	本-阿莫斯	4.42	本-阿莫斯	曼联	门将	英格兰
+ get_nba_score

    网址：<https://nba.hupu.com/stats/teams>

    获取虎扑体育中NBA球队数据排名详细信息

    例如：1   勇士	47.7%	41.8	87.6	33.8%	10.2	30.2	83.0%	18.0	21.7	46.6	9.3	37.3	27.2	12.77	8.15	5.31	18.69	111.8

### 注意事项：

1. 在python中，需要注意编码问题在2.7版本中，由于爬取的内容默认保存为Unicode字符，往往在直接进行传递的是导致编码错误，因此经常需要对获取的内容进行编码格式的转换，尤其是在写文件write的时候.python2.7之前，不支持关键词参数，所以使用decode('编码方式', errors='ignore')会导致错误直接使用decode('编码方式', 'ignore')就可以

2. 模拟登陆问题：进行爬虫的时候，可能需要模拟浏览器登陆

3. 爬虫注意的问题：

    头信息问题：在爬取的过程中，为了模拟requests请求，往往需要添加头信息，我们可以提前给出一些有效头信息，然后添加到列表中，进行随机选择；python提供了第三方库fake-useragent库，可以方便快捷的伪造头信息

#### 在项目中，经常用到的python第三方库：

fake-useragent  提供伪造的头信息

selenium        自动化测试脚本，控制浏览器进行一些重复的行为

phantomjs       无界面的浏览器，与selenium结合，进行模拟浏览器行为，常用来下载动态js加载的网页

bs4             BeautifulSoup库，用来解析下载的网页内容

Chrome浏览器爬虫插件：JSONView