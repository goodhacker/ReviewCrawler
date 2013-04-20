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
url = "http://detail.tmall.com/item.htm?id=16597410035"

def printInfo(info):
    print "info:"
    info.decode("gbk").encode("utf-8")
    print info[info.find("(")+1:info.find(")",-1)-2].replace("\n","")
    j = json.loads(unicode(info[info.find("(")+1:info.find(")",-1)-2].replace("\n",""),"gbk"))
    print j
    print j["maxPage"]
    print j["currentPageNum"]


def findIdString(script,string):
    start = script.find(string)
    quotation = script[start-1]
    idStart = script.find(quotation,script.find(":",start))
    sId = script[idStart+1:script.find(quotation,idStart+1)]
    return sId

req = urllib2.Request(url = url,headers = headers)
socket.setdefaulttimeout(20)
response = urllib2.urlopen(req)
coding= response.headers.getparam("charset")
page=response.read()
page=page.decode(coding).encode('utf-8')
soup=BeautifulSoup(page)

print soup.find("form",id="J_FrmBid")
print soup.find("form",id="J_FrmBid").find_next_sibling()
script = soup.find("form",id="J_FrmBid").find_next_sibling().get_text()

d = {}
d['spuId'] = findIdString(script,'spuId')
d['sellerId'] = findIdString(script,'userId')
d['itemId'] = findIdString(script,'itemId')

print d

#items=soup.find(id="list-content").find_all(class_="list-item")
#for item in items[:2]:
#    title = item.find(class_ = "summary").find("a")["title"]
#    print title
#    sellerIdstr = item.find(class_="shopinfo")["dataurl"]
#    begin = sellerIdstr.find("?sid")+5
#    sellerId = sellerIdstr[begin:sellerIdstr.find("&",begin)]
#    print sellerId
#    price = item.find(class_="price").find("em")
#    print price
#    print price.string
#    picurl = item.find(class_="photo").find('a').find('span').find('img')['data-ks-lazyload']
#    print picurl


    
#findIdString(script,'spuId')
#findIdString(script,'userId')
#findIdString(script,'itemId')


