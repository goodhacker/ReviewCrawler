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
        pass
    
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

    def getReviewsFromPage(self,title,params):
        cp = 1        
        for cp in range(1,15000):
            #if cp%50 == 0:
            #   reactor.run()
            #   time.sleep(2)
            print cp
            params["currentPageNum"] = cp
            #info = self.getPageFromUrl('http://rate.taobao.com/feedRateList.htm?',params = params)
            url = self.generateReviewUrl('http://rate.taobao.com/feedRateList.htm?',params = params)
            print url
            page = getPage(url,timeout=20)
            page.addCallback(self.parseReviewJson)
            page.addCallback(self.writeToCSV,title=title)
            page.addErrback(self.getPageError,cp)
        reactor.run()

    def parseReviewJson(self,info):
        dataL = []
        try:
            j = json.loads(unicode(info[info.find("(")+1:info.find(")",-1)-2].replace("\n",""),"gbk"))
        except Exception,e:
            print e
        if j["maxPage"] == j["currentPageNum"]:
            #raise Exception("stop")
            return dataL
        for item in j["comments"]:
            if len(item["content"]) < 15:
                continue
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

        return dataL

class TmallCrawler(BaseReviewCrawler):

    def __init__(self):
        pass
    
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

    def getReviewsFromPage(self,title,params):
       info = self.getPageFromUrl('http://rate.tmall.com/list_detail_rate.htm?',params = params)
       j = json.loads("{"+info+"}")
       currentPage = j["rateDetail"]["paginator"]["page"]
       lastPage = j["rateDetail"]["paginator"]["lastPage"]
       
       for cp in range(currentPage,lastPage):
           print cp
           if cp%100 == 0:
              time.sleep(60)
          # if cp > 2:
          #     break
           params["currentPage"] = cp
          # info = self.getPageFromUrl('http://rate.tmall.com/list_detail_rate.htm?',params = params)
           url=self.generateReviewUrl('http://rate.tmall.com/list_detail_rate.htm?',params = params)        
           page=getPage(url,timeout=20)
           page.addCallback(self.parseReviewJson)           
           page.addCallback(self.writeToCSV,title=title)
           page.addErrback(self.getPageError,cp)
           
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

crawler = TmallCrawler()
crawler.crawl("http://detail.tmall.com/item.htm?id=14944940915")
