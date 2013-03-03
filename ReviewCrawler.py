#encoding=utf-8
from bs4 import BeautifulSoup
import urllib
import urllib2
import re
import time
import socket
import json
import csv
import codecs
import cStringIO

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.91 Safari/537.11"
}

class TaobaoCrawler:
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
            page = self.getPageFromUrl(visitUrl)
            soup = BeautifulSoup(page)
            if visitUrl.find("tmall") > -1:               
                title = self.getTmallItemTitle(soup)
                print title
                params = self.crawlTmallQueryParameters(soup)
                print params
                dataList = self.getReviewsFromTmallPage(params)
                self.writeToCSV(title,dataList)
                #continue
            else:
                title = self.getTaobaoItemTitle(soup)
                print title
                params = self.crawlTaobaoQueryParameters(soup)
                print params
                dataList = self.getReviewsFromTaobaoPage(params)
                self.writeToCSV(title,dataList)
            #将url放入已访问的url中
            self.linkQuence.addVisitedUrl(visitUrl)
     #写入文件       
    def writeToCSV(self,title,dataL):
        fieldnames = ['reviewContent', 'reviewTime', 'userNick', 'userId','userLink','appendReview','appendTime']
        #dict_writer = csv.DictWriter(codecs.open(title+".csv", "w","utf-8"), fieldnames=fieldnames)
    #   dict_writer.writerow(fieldnames) # CSV第一行需要自己加入
        f = open(title+'.csv','w')
        dict_writer = DictUnicodeWriter(f,fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(dataL)  # rows就是表单提交的数据
        dataL=[]
        f.close()
        
    #产品标题    
    def getTmallItemTitle(self,soup):
        return soup.find(id="mainwrap").find(id="detail").find("a").get_text()
    def getTaobaoItemTitle(self,soup):
        return soup.find(id="page").find(id="detail").find("h3").get_text()
        
    def crawlTmallQueryParameters(self,soup):     
        script = soup.find("div",id="J_itemViewed").find_next().get_text()
        d = {}
        d['spuId'] = self.findIdString(script,'spuId')
        d['sellerId'] = self.findIdString(script,'userId')
        d['itemId'] = self.findIdString(script,'itemId')
        return d

    def findIdString(self,script,string):
        start = script.find(string)
        quotation = script[start-1]
        idStart = script.find(quotation,script.find(":",start))
        sId = script[idStart+1:script.find(quotation,idStart+1)]
        return sId

    def crawlTaobaoQueryParameters(self,soup):
        reviewUrl = soup.find("div",id="reviews",class_="J_DetailSection").get("data-listapi")
        #print soup.find("div",id="reviews",class_="J_DetailSection")
        print reviewUrl
        paramList = reviewUrl[reviewUrl.find("?")+1:].split("&")
        d = {}
        for param in paramList:
            p = param.split("=")
            d[p[0]] = p[1]
        for key in d.keys():
            if key not in ["userNumId","auctionNumId"]:
                d.pop(key)
        return d

    def getPageFromUrl(self,url,params = None,timeout=1000,coding=None):
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
            else:
                page=response.read()
                page=page.decode(coding,'ignore').encode('utf-8')
            return page       
        except Exception,e:
            print e
        
    
    #获取网页源码
    def crawlReviews(self,url,timeout=100,coding=None):
      #  try:
            #socket.setdefaulttimeout(timeout)
            req = urllib2.Request(url=url,headers = headers)
            response = urllib2.urlopen(req)
            if coding is None:
                coding= response.headers.getparam("charset")
            if coding is None:
                page=response.read()
            else:
                page=response.read()
                page=page.decode(coding).encode('utf-8')
            #print response.url
            self.getReviewsInPage(url,page)         
       # except Exception,e:
       #     print e
       
    def getReviewsFromTmallPage(self,params):
       info = self.getPageFromUrl('http://rate.tmall.com/list_detail_rate.htm?',params = params)
       j = json.loads("{"+info+"}")
       currentPage = j["rateDetail"]["paginator"]["page"]
       lastPage = j["rateDetail"]["paginator"]["lastPage"]
       dataL = []
       for cp in range(currentPage,lastPage):
           print cp
          # if cp > 2:
          #     break
           params["currentPage"] = cp
           info = self.getPageFromUrl('http://rate.tmall.com/list_detail_rate.htm?',params = params)
           j = json.loads("{"+info+"}")
           for item in j["rateDetail"]["rateList"]:
               d = {}
               if item["useful"]:
                   d["userNick"] = item["displayUserNick"]
                   d["userId"] = unicode(item["displayUserNumId"])
                   d["reviewContent"] = item["rateContent"]
                   d["reviewTime"] = item["rateDate"]
                   d["appendReview"] = ""
                   d["appendTime"] = ""
                   if len(item["appendComment"]) > 0:
                       d["appendReview"] = item["appendComment"]["content"]
                       d["appendTime"] = item["appendComment"]["commentTime"]
                   dataL.append(d)
                 #  print type(d["userNick"])
                 #  print type(d["userId"])
                 #  print type(d["reviewContent"])
                 #  print type(d["reviewTime"])
                 #  print "******************************************"
                   
       return dataL
    
    def getReviewsFromTaobaoPage(self,params):
        cp = 1
        dataL = []
        while True:
            print cp
            params["currentPageNum"] = cp
            info = self.getPageFromUrl('http://rate.taobao.com/feedRateList.htm?',params = params)
            if type(info) == None:
                print "info NoneType"
                continue
            #print info[info.find("(")+1:info.find(")",-1)-2]
            try:
                j = json.loads(info[info.find("(")+1:info.find(")",-1)-2].replace("\n","")
)
            except Exception,e:
                print e
                print "Error %d"%cp
                cp = cp+1
                continue
            if j["maxPage"] == j["currentPageNum"]:
                break
            for item in j["comments"]:
                d = {}
                d["userNick"] = item["user"]["nick"]
                d["userId"] = unicode(item["user"]["userId"])
                d["userLink"] = item["user"]["nickUrl"]
                d["reviewContent"] = item["content"]
                d["reviewTime"] = item["date"]
                d["appendReview"] = ""
                #d["appendTime"] = ""
                #print item["append"]
                if item["append"] is not None:
                    d["appendReview"] = item["append"]["content"]
                       #d["appendTime"] = item["appendComment"]["commentTime"]
                dataL.append(d)
            cp = cp+1

        return dataL
                      
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

#This class from http://stackoverflow.com/questions/5838605/python-dictwriter-writing-utf-8-encoded-csv-files
class DictUnicodeWriter(object):

    def __init__(self, f, fieldnames, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.DictWriter(self.queue, fieldnames, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, D):
        for k in D.keys():
            self.writer.writerow({k:D[k].encode("utf-8")})
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for D in rows:
            self.writerow(D)

    def writeheader(self):
        self.writer.writeheader()
        
    
def main(seeds):
    craw=TaobaoCrawler(seeds)
    craw.crawling(seeds)

if __name__=="__main__":
    firstUrl = "http://s8.taobao.com/search?spm=a230z.1.0.166.JaXcjp&q=%C5%AE%B0%FC&style=grid&atype=b&isnew=2&olu=yes&promoted_service4=4&pid=mm_33705144_3435898_11134072&tab=all&sort=sale-desc"
    main(firstUrl)

   # http://rate.tmall.com/list_detail_rate.htm?itemId=17599831517&spuId=209936077&sellerId=1036065909&currentPage=0
#http://rate.taobao.com/feedRateList.htm?userNumId=36415070&auctionNumId=17041248927&currentPageNum=1&rateType=&orderType=sort_weight
