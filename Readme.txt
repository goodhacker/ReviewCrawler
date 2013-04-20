好像在windows上不存在编码问题了，不过天猫的页面改了，代码我还是跟着改了一些。
爬下来的数据都是以utf-8的形式存储在.csv里，用excel打开是乱码。我自己有EditPlus这类文本编辑器的辅助

语言：python2.7  python3不行哦

第三方类库：
Beautifulsoup4  http://www.crummy.com/software/BeautifulSoup/bs4/download/
twisted  http://twistedmatrix.com/trac/


主要文件：

ReviewCrawler.py 
也是运行文件
这个文件主要是分析商品列表界面，获得商品的基本信息，比如商品名称，商品id，图片地址，价钱等。然后通过这些信息找到某商品的页面。
爬过的商品地址在visited.dat里，下回就不爬了
可以改的参数有：
1. 最下面的firstUrl，是你要爬的商品列表的地址，这个地址是在淘宝上搜索某关键字后，点击搜索后获得的地址
比如这种，界面应该是这样的：http://s8.taobao.com/search?q=%CA%D6%B1%ED&pid=mm_34012603_3435519_11130749&commend=all&ssid=s5-e
2. 最上面的BASE_INFO_FILE，BASE_INFO_PATH，是存储商品基本信息（比如标题，价钱，图片地址等）文件地址
3. ITEM_NUM 要爬的商品数量，最多40（一页最多就40个吧

BaseReviewCrawler.py
淘宝有天猫和淘宝两种店，界面是不一样的，所以一些基本操作比如打开url，写入文件什么的操作都在BaseReviewCrawler里，
与页面相关的都在SubReviewCrawler里
可以改的参数：
1. CSV_PATH  csv文件地址
2. writeToCSV函数，往csv写入什么信息的处理，fieldnames是信息的列标题

SubReviewCrawler.py
有Taobao和Tmall两个类
可以改的：
1. TIMEOUT：单位s,超过这个时间这个页面就重爬
2. 每个类的self.jsonPath，json文件的存储位置，或许不需要留json，但是这块不要乱删
3. 每个类的parseReviewJson函数，解析评论的json文件，给个例子：
tmall：http://rate.tmall.com/list_detail_rate.htm?itemId=8140241528&spuId=123185051&sellerId=525798483&order=0&forShop=1&_ksTS=1366450096661_1004&callback=jsonp1005
taobao：http://rate.taobao.com/feedRateList.htm?callback=jsonp_reviews_list&userNumId=811030409&auctionNumId=15043528059&siteID=7&currentPageNum=1&rateType=&orderType=sort_weight&showContent=1&attribute=

DictUnicodeWriter.py
写入CSV过程的封装，基本不用管

removeDuplicate.py
我也不知道为什么有时候会重复爬，反正跑一下这个就行。里面的地址改成csv所在地址

其他文件忽略

因为有超时异常处理，所以基本参数设好了开着跑就行。但是其他地方没抓异常，所以崩了就只能改代码了。