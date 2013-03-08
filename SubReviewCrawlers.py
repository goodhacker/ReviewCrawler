#encoding=utf-8
import json
import time
from bs4 import BeautifulSoup
from twisted.internet import reactor,defer
from twisted.web.client import getPage
from twisted.web.error import Error
from BaseReviewCrawler import BaseReviewCrawler

class TaobaoCrawler(BaseReviewCrawler):

    def __init__(self):
        self.urlPrefix = 'http://rate.taobao.com/feedRateList.htm?'
        self.running = True
    
    def getItemTitle(self,soup):
        return soup.find(id="page").find(id="detail").find("h3").get_text().encode("utf-8")

    def crawlQueryParameters(self,soup):
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
    
    @defer.deferredGenerator
    def getReviewsFromPage(self,title,params):
        
        def deferred1(page):
            d = defer.Deferred()
            reactor.callLater(1,d.callback,self.parseReviewJson(page))
            return d

        def deferred2(dataL,title):
            d = defer.Deferred()
            reactor.callLater(1,d.callback,self.writeToCSV(dataL,title=title))
            return d
        
        cp = 1        
        #for cp in range(1,15000):
        while self.running:
            print cp
            params["currentPageNum"] = cp
            #info = self.getPageFromUrl('http://rate.taobao.com/feedRateList.htm?',params = params)
            url = self.generateReviewUrl(self.urlPrefix,params = params)
            print url
            
            wfd = defer.waitForDeferred(getPage(url,timeout=10))
            yield wfd
            page = wfd.getResult()
            wfd = defer.waitForDeferred(deferred1(page))
            yield wfd
            dataList = wfd.getResult()
            wfd = defer.waitForDeferred(deferred2(dataList,title))
            yield wfd
            cp = cp+1
        reactor.stop()

    def parseReviewJson(self,info):
        dataL = []
        try:
            j = json.loads(unicode(info[info.find("(")+1:info.find(")",-1)-2].replace("\n",""),"gbk"))
        except Exception,e:
            print e
        if j["maxPage"] == j["currentPageNum"]:
            self.running = False
            return dataL
        for item in j["comments"]:
            if len(item["content"]) < 15:
                continue
            d = {}
            d["reviewContent"] = item["content"]
            d["reviewTime"] = item["date"]
            d["userNick"] = item["user"]["nick"]
            d["userId"] = unicode(item["user"]["userId"])
            d["userLink"] = item["user"]["nickUrl"]        
            d["appendReview"] = ""
            #d["appendTime"] = ""
            #print item["append"]
            if item["append"] is not None:
                d["appendReview"] = item["append"]["content"]
               
            dataL.append(d)

        return dataL

class TmallCrawler(BaseReviewCrawler):

    def __init__(self):
        self.urlPrefix = "http://rate.tmall.com/list_detail_rate.htm?"
    
    def getItemTitle(self,soup):
        return soup.find(id="mainwrap").find(id="detail").find("a").get_text().encode("utf-8")

    def crawlQueryParameters(self,soup):     
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

    @defer.deferredGenerator
    def getReviewsFromPage(self,title,params):
        print "getReviewsFromPage"

        def deferred1(page):
            d = defer.Deferred()
            reactor.callLater(1,d.callback,self.parseReviewJson(page))
            return d

        def deferred2(dataL,title):
            d = defer.Deferred()
            reactor.callLater(1,d.callback,self.writeToCSV(dataL,title=title))
            return d

        info = self.getPageFromUrl('http://rate.tmall.com/list_detail_rate.htm?',params = params)
        j = json.loads("{"+info+"}")
        currentPage = j["rateDetail"]["paginator"]["page"]
        lastPage = j["rateDetail"]["paginator"]["lastPage"]
        
        for cp in range(currentPage,lastPage):
            print cp
          
            params["currentPage"] = cp
            # info = self.getPageFromUrl('http://rate.tmall.com/list_detail_rate.htm?',params = params)
            url=self.generateReviewUrl(self.urlPrefix,params = params)        
           
            wfd = defer.waitForDeferred(getPage(url,timeout=10))
            yield wfd
            page = wfd.getResult()
            wfd = defer.waitForDeferred(deferred1(page))
            yield wfd
            dataList = wfd.getResult()
            wfd = defer.waitForDeferred(deferred2(dataList,title))
            yield wfd
        reactor.stop()
           
    def parseReviewJson(self,info):
        dataL = []
        j = json.loads("{"+unicode(info,"gbk")+"}")
        for item in j["rateDetail"]["rateList"]:
            d = {}
            if item["useful"]:
                if item["dsr"] < 4:
                    continue
                if len(item["rateContent"]) < 15:
                    continue
                d["reviewContent"] = item["rateContent"]
                d["reviewTime"] = item["rateDate"]
                d["userNick"] = item["displayUserNick"]
                d["userId"] = unicode(item["displayUserNumId"])
                d["userLink"] = item["displayUserLink"]
                d["appendReview"] = ""
                d["appendTime"] = ""
                if len(item["appendComment"]) > 0:
                    d["appendReview"] = item["appendComment"]["content"]
                    d["appendTime"] = item["appendComment"]["commentTime"]
                dataL.append(d)
                print d["userNick"]
                print d["userId"]
                print d["reviewContent"]
                print d["reviewTime"]
                print "******************************************"
        return dataL

crawler = TmallCrawler()
crawler.crawl("http://detail.tmall.com/item.htm?id=14944940915")

#crawler2 = TaobaoCrawler()
#crawler2.crawl("http://item.taobao.com/item.htm?id=17180958841")
