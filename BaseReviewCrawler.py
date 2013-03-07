#encoding=utf-8
import DictUnicodeWriter

class BaseReviewCrawler:
    def __init__(self,url):
        baseUrl = url
             
    def writeToCSV(self,dataL,title):
        if len(dataL)==0:
            return
        fieldnames = ['reviewContent', 'reviewTime', 'userNick', 'userId','userLink','appendReview','appendTime']
        #dict_writer = csv.DictWriter(codecs.open(title+".csv", "w","utf-8"), fieldnames=fieldnames)
    #   dict_writer.writerow(fieldnames) # CSV??????????????????
        f = open(title+'.csv','w')
        print "writeToCSV"
        print title
        print dataL
        dict_writer = DictUnicodeWriter(f,fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(dataL)  # rows??????????????????
        dataL=[]
        f.close()

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

    def crawlReviews(self,url,timeout=20,coding=None):
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
       
    def generateReviewUrl(self,prefix,params):
        for key in params.keys():
            prefix=prefix+"%s=%s"%(key,params[key])+"&"
        return str(prefix[:-1])

    def getItemTitle(self,soup):
        raise NotImplementedException

    def crawlQueryParams(self,soup):
        raise NotImplementedException

    def getReviewsFromPage(self,title,params):
        raise NotImplementedException

    def parseReviewJson(self,Json):
        raise NotImplementedException

    def crawl():
        page = self.getPageFromUrl(self.baseUrl)
        soup = BeautifulSoup(page)
        title = self.getItemTitle(soup)
        print title.decode("utf-8").encode("gb2312")
        params = self.TmallQueryParameters(soup)
        print params
        dataList = self.getReviewsFromPage(title,params)
        # self.writeToCSV(title,dataList)

