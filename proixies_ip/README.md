# 代理IP池脚本

平台：
    python2.7+PyCharm
代理ip格式：
    <http://xxxxxx:xxx>  :  协议://ip:port
脚本注释：
    __init__:
        page:=3 默认爬取代理ip网站的页数
        filename:='all.proxies.txt' 默认写有效代理ip的文件名
        作用：类进行初始化的时候，直接爬去默认开启的代理ip网站的ip，将其写入列表proxies
    get_init:
        page:=3 代理ip网站的翻页数
        作用：手动初始化，便于代理ip池的维护
    write_all_proxies:
        作用：将有效的代理ip写入本地文件，便于其他程序调用
    get_all_proixy:
        作用：返回所有有效代理ip
    get_headers:
        作用：利用第三方库fake-useragent返回伪造的头信息
    get_***_proxies：
        该系列的方法为抓取代理ip的方法，抓取的网站列表有：
            <http://www.xicidaili.com/nt>
            <https://www.kuaidaili.com/free/inha/>
            <http://www.data5u.com/free/gnpt/index.shtml>
            <http://www.66ip.cn/>
            <http://www.goubanjia.com/>
            <http://www.mimiip.com/gngao/>
            <http://www.ip3366.net/free/>
            <http://www.iphai.com/free/>
            <http://ip.jiangxianli.com/>
            <http://www.gatherproxy.com/zh/proxylist/anonymity/>              推荐：【墙外】
            <https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1>          墙外网站
            <https://proxy.coderbusy.com/classical/country/cn.aspx?page=1>    经常宕机
            <http://cn-proxy.com/archives/218>                                墙外网站
    verify_proxies:
        多进程+队列验证代理ip的有效性
    verify_one_proxy:
        通过访问百度的情况，验证代理ip的有效性[多进程+队列]
    verify_ip：
        通过访问百度，验证代理ip的有效性[验证单个代理ip有效性+删除无效ip]
    api:
        以字典形式，返回一个代理ip
备注：
    1.在爬取的代理中，有三个墙外的网站，需要翻墙才可以访问，否则将其注释掉
    2.在访问gatherproxy网站的时候，使用了selenium+Phantomjs来进行模拟浏览器访问，如果不想安装Phantomjs可以browser = webdriver.PhantomJS()替换为browser = webdriver.Chrome()/browser = webdriver.Firefox()
    3.将爬取的代理ip存在了self.proxies中，可以直接访问该变量或者通过get_all_proixy方法获取所有的代理ip
    4.对获取的代理ip进行验证，通过多进程+队列的方式实现
    5.可以后续通过verify_ip方法验证保存的ip是否有效，验证的同时会删除已经失效的代理ip。
    6.可以将该脚本放入其他项目中，通过该类的实例，直接调用api方法即可得到有效的代理ip
第三方库：
    fake_useragent
    requests
    bs4
    selenium
    lxml