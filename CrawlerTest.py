#encoding=utf-8
from bs4 import BeautifulSoup
import urllib2
import re
import time
import socket
from twisted.internet import reactor
from twisted.web.client import getPage
import json


headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.91 Safari/537.11"
}
url = "http://rate.taobao.com/feedRateList.htm?currentPageNum=2&userNumId=83244358&auctionNumId=13533367346&rateType=1"

def printInfo(info):
    print "info:"
    info.decode("gbk").encode("utf-8")
    print info[info.find("(")+1:info.find(")",-1)-2].replace("\n","")
    j = json.loads(unicode(info[info.find("(")+1:info.find(")",-1)-2].replace("\n",""),"gbk"))
    print j
    print j["maxPage"]
    print j["currentPageNum"]

def getError(err):
    print err
    reactor.stop()
    
d = getPage(url)
d.addCallback(printInfo)
d.addErrback(getError)
reactor.run()


#req = urllib2.Request(url = url,headers = headers)
#socket.setdefaulttimeout(20)
#response = urllib2.urlopen(req)
#coding= response.headers.getparam("charset")
#page=response.read()
#page=page.decode(coding).encode('utf-8')
#soup=BeautifulSoup(page)

#title = soup.find(id="page").find(id="detail").find("h3").get_text()
#print title.encode('utf-8')

#script = soup.find("div",id="J_itemViewed").find_next().get_text()

def findIdString(script,string):
    start = script.find(string)
    quotation = script[start-1]
    idStart = script.find(quotation,script.find(":",start))
    sId = script[idStart+1:script.find(quotation,idStart+1)]
    return sId
    
#findIdString(script,'spuId')
#findIdString(script,'userId')
#findIdString(script,'itemId')


