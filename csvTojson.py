#encoding=utf-8
import csv
import json
import os
import codecs
import sys

def writeJsonToFile(jsondict,path,name):
    print "write to %s.json\n"%name
    path = path.strip("/")
    if not os.path.exists(path) and len(path) > 0:
        os.mkdir(path)
    with codecs.open(path+"/"+str(name)+".json","w") as outfile:
        outfile.write(json.dumps(jsondict,ensure_ascii=False,encoding = "utf-8"))
        outfile.flush()

print sys.getfilesystemencoding()
        
csvPath = "CSV/"
infoname = "itemBaseInfo.csv"
infocsv = csv.reader(codecs.open(infoname,'r'),delimiter="\t")
infofields = infocsv.next()
infodd = {}
for row in infocsv:
    infoD={}
    for i in range(0,len(infofields)): 
        infoD[infofields[i]] = row[i].decode("utf-8").encode("utf-8","ignore")
    infodd[row[1]] = infoD

filenames = os.listdir(csvPath)
jsonid=0
for filename in filenames:
    name = ""
    #if filename.split(".")[1] == "csv2" or filename.split(".")[1] == "csvaa":
    #    name = filename.split(".")[0]
    #else:continue

    if not filename.split(".")[1] == "csv2":
        continue
    else:
        name = filename.split(".")[0]

    print "Converting %s"%filename
    csvfile = csv.reader(codecs.open(csvPath+filename,'r'),delimiter="\t")
    fieldnames = csvfile.next()
    #fieldnames = ['id','reviewContent', 'reviewTime', 'degree','userNick', 'userId','userLink','appendId','appendReview','appendTime']
    #infoD = infodd[name]
    d = infodd[name] 
    #d["itemId"] = str(name)
    #d["title"] = name.decode("gbk").encode("utf-8") 
    #d["title"] = infoD['title'] 
    d["reviews"] = []
    #Put every review into reviewList
    for row in csvfile:
        dd = {}
        for j in range(0,len(fieldnames)):
            import chardet
            try:
                dd[fieldnames[j]] = row[j].decode("utf-8").encode("utf-8","ignore")
               # print row[j]
               # print chardet.detect(dd[fieldnames[j]])
            except Exception,e:
                print "\n\n"
                print e
                print row[j]
                print chardet.detect(row[j])
        d["reviews"].append(dd)
    
    writeJsonToFile(d,"Json/",name)
    jsonid = jsonid+1
