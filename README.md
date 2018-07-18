# InternRecord
实习期间看到的、遇到的、学到的东西，进行记录下

记录包括：
1.豆瓣电影爬虫
    1)douban-movie-spider
    2)nowing-coming-movie
2.网易云音乐爬虫
    1)scrapy-project
    2)stan-alone
3.qq音乐爬虫
    1)qq-music-scrapy
        利用scrapy框架，爬取指定文件中包含的歌手的所有歌曲
        歌手文件：singer.txt    [格式：歌手]    [备注：singer.txt后两列暂时无用]
        爬取结果：result.txt    [格式：歌曲\t歌手\t专辑]
        爬虫运行：python entrypoint.py
        版本：3.6版本
    2)qq-music-singer-hot-song
        利用scrapy框架，爬取指定歌手的热门歌曲，整体流程同爬取所有歌手歌曲的流程
        歌手文件：result.txt    [格式：歌手]
        结果文件：singer_song.txt   [格式：歌曲\t歌手\t专辑]
        爬虫运行：python entrypoint.py
        版本：2.7版本
4.虎扑体育爬虫
    1)get_cba_score
    https://cba.hupu.com/players/
        获取CBA球队-序号-球员-身高-体重-位置-出生日期的信息
        例如：
        广东华南虎	29	李佳益	208CM/6尺10寸	115KG / 253磅	中锋	1997年9月2日
    2)NBA_Spyder
    http://china.nba.com/static/data/league/playerlist.json
        获取NBA主流球队中球员-球队-位置-国家的信息，
        例如：
        凯尔 安德森	灰熊	前锋	美国
    3)get-football_score
    https://soccer.hupu.com/g/players/
        获取国际足球中英超、西甲、意甲、德甲和法甲中球队的球员数据信息
        例如：
        曼联	本-阿莫斯	4.42	本-阿莫斯	曼联	门将	英格兰
    4)get_nba_score
    https://nba.hupu.com/stats/teams
        获取虎扑体育中NBA球队数据排名详细信息
        例如：
        1	勇士	47.7%	41.8	87.6	33.8%	10.2	30.2	83.0%	18.0	21.7	46.6	9.3	37.3	27.2	12.77	8.15	5.31	18.69	111.8	

注意事项：
1.在python中，需要注意编码问题在2.7版本中，由于爬取的内容默认保存为Unicode字符，往往在直接进行传递的是导致编码错误，因此经常需要对获取的内容进行编码格式的转换，尤其是在写文件write的时候

