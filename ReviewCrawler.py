#encoding=utf-8
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import time
import socket
from SubReviewCrawlers import TaobaoCrawler
from SubReviewCrawlers import TmallCrawler

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.91 Safari/537.11"
}

class Crawler:
    def __init__(self,seed):
        #使用种子初始化url队列
        self.linkQuence=linkQuence()
        seeds = self.getReviewPageUrl(seed)
        if isinstance(seeds,str):
            self.linkQuence.addUnvisitedUrl(seeds)
        if isinstance(seeds,list):
            for i in seeds:
                self.linkQuence.addUnvisitedUrl(i)
        print "Add %d url to list\n"%len(seeds)

    #获得商品界面连接
    def getReviewPageUrl(self,seed):
        req = urllib2.Request(url=seed,headers = headers)
        content = urllib2.urlopen(req)
        soup=BeautifulSoup(content)
        items=soup.find(id="list-content").find_all(class_="list-item")
        urls = []
        for item in items:
            item_data = item.find(class_="seller").find("span")
            item_id = item_data["data-item"]
            if self.isTmallItem(item):
                urls.append("http://detail.tmall.com/item.htm?id=%s"%item_id)
            else: urls.append("http://item.taobao.com/item.htm?id=%s"%item_id)
        return urls

    def isTmallItem(self,item):
        return True if item.find(class_="mall-icon") else False
    
    #抓取过程主函数
    def crawling(self,seeds):
        #循环条件：待抓取的链接不空且专区的网页不多于crawl_count
        while self.linkQuence.unVisitedUrlsEnmpy() is False:
            #队头url出队列
            visitUrl=self.linkQuence.unVisitedUrlDeQuence()
            if visitUrl is None or visitUrl=="":
                continue
            print visitUrl
               
            if visitUrl.find("tmall") > -1:
                crawler = TmallCrawler()
                crawler.crawl(visitUrl)
            else:
                crawler = TaobaoCrawler()
                crawler.crawl(visitUrl)             
            #将url放入已访问的url中
            self.linkQuence.addVisitedUrl(visitUrl)
 
    def getPageFromUrl(self,url,params = None,timeout=20,coding=None):
        try:
            socket.setdefaulttimeout(timeout)
            if params:
                #print params
                req = urllib2.Request(url=url, data=urllib.urlencode(params), headers=headers)
            else:
                req = urllib2.Request(url=url,headers=headers)
            response = urllib2.urlopen(req)
            if coding is None:
                coding= response.headers.getparam("charset")
            if coding is None:
                page=response.read()
                print "coding = None"
            else:
                page=response.read()
                page=page.decode(coding).encode('utf-8')
                print "coding = %s"%coding
            return page       
        except Exception,e:
            print e  

  
class linkQuence:
    def __init__(self):
        #已访问的url集合
        self.visted=[]
        visitedList = QuenceFileIO().readVisited()
        print visitedList
        self.visted.extend(visitedList)
        #待访问的url集合
        self.unVisited=[]
    #获取访问过的url队列
    def getVisitedUrl(self):
        return self.visted
    #获取未访问的url队列
    def getUnvisitedUrl(self):
        return self.unVisited
    #添加到访问过得url队列中
    def addVisitedUrl(self,url):
        self.visted.append(url)
        QuenceFileIO().addVisited(url)
    #移除访问过得url
    def removeVisitedUrl(self,url):
        self.visted.remove(url)
    #未访问过得url出队列
    def unVisitedUrlDeQuence(self):
        try:
            return self.unVisited.pop()
        except:
            return None
    #保证每个url只被访问一次
    def addUnvisitedUrl(self,url):
        if url!="" and url not in self.visted and url not in self.unVisited:
            self.unVisited.insert(0,url)
    #获得已访问的url数目
    def getVisitedUrlCount(self):
        return len(self.visted)
    #获得未访问的url数目
    def getUnvistedUrlCount(self):
        return len(self.unVisited)
    #判断未访问的url队列是否为空
    def unVisitedUrlsEnmpy(self):
        return len(self.unVisited)==0

class QuenceFileIO:
    def __init__(self):
        pass
    def addVisited(self,url):
        f=open('visited.dat','a')
        f.write(url+'\n')
        f.flush()
        f.close()
    def readVisited(self):
        f=open('visited.dat','r')
        urls = []
        while True:
            line = f.readline().strip('\n')
            if not line:
                break
            urls.append(line)
        f.close()
        return urls
        
    
def main(seeds):
    craw=Crawler(seeds)
    craw.crawling(seeds)

if __name__=="__main__":
    firstUrl = "http://s8.taobao.com/search?spm=a230z.1.0.166.JaXcjp&q=%C5%AE%B0%FC&style=grid&atype=b&isnew=2&olu=yes&promoted_service4=4&pid=mm_33705144_3435898_11134072&tab=all&sort=sale-desc"
    main(firstUrl)

   # http://rate.tmall.com/list_detail_rate.htm?itemId=17599831517&spuId=209936077&sellerId=1036065909&currentPage=0
#http://rate.taobao.com/feedRateList.htm?userNumId=36415070&auctionNumId=17041248927&currentPageNum=1&rateType=&orderType=sort_weight
