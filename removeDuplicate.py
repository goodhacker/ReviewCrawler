#encoding=UTF-8
import csv
import pdb
import os
import codecs
import re

csvPath="CSV/"
filenames = os.listdir(csvPath)
test = re.compile(".*\.csv$", re.IGNORECASE)           
filenames = filter(test.search, filenames)   

for filename in filenames:
    print "Processing %s"%filename
    csvfile = csv.reader(codecs.open(csvPath+filename,'r'),delimiter="\t")
    fieldnames = csvfile.next()
    nickIndex = fieldnames.index('userNick')
    contentIndex = fieldnames.index('reviewContent')
    duplicateLine = []
    rowNum = 1
    d = {}
    newList = []
    for row in csvfile:
        rowNum = rowNum + 1
        if not row:
            break
        nick = row[nickIndex]
        content = row[contentIndex]
        if d.has_key(nick):
            if content in d[nick]:
               # print filename
               # print rowNum
               # print content
               # for c in d[nick]:
               #     print c
               # print rowNum 
                duplicateLine.append(rowNum)
            else:
                newList.append(row)
                d[nick].append(content)
        else:
            d[nick] = []
            newList.append(row)
            d[nick].append(content)
    print len(duplicateLine)
    print "Write to %s"%(filename+"2")
    csvwriter = csv.writer(codecs.open(csvPath+filename+"2",'w'),delimiter="\t")
    csvwriter.writerow(fieldnames)
    csvwriter.writerows(newList)



