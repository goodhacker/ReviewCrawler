#encoding=utf-8
from bs4 import BeautifulSoup
import urllib2
import re
import time

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.91 Safari/537.11"
}
url = "http://item.taobao.com/item.htm?id=14900370608"
req = urllib2.Request(url = url,headers = headers)
response = urllib2.urlopen(req)
coding= response.headers.getparam("charset")
page=response.read()
page=page.decode(coding).encode('utf-8')
soup=BeautifulSoup(page)
print soup.find(id="page")
print "***************************************"
print soup.find(id="page").find(id="detail")
print soup.find(id="page").find(id="detail").find("h3").get_text()
title = soup.find(id="page").find(id="detail").find("h3").find("span").get_text()


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


