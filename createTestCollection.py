from pymongo import MongoClient
import os
 
connection = MongoClient()
reviewdb = connection.reviewdb
review_train = reviewdb['review_train']

#jsonPath="/home/yang/ReviewCrawler/Json/"

jsonPath="../data/Json/Test/"
filenames = os.listdir(jsonPath)
for filename in filenames:
    print filename
    if filename.find(".") == -1:
        continue
    name = filename.split('.')[0]
    review_train.remove({'itemId':name})
    os.system("mongoimport -d reviewdb -c review_test --file %s"%jsonPath+filename)

