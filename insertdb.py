import connect2db
import json
import pymongo
import csv
import re

# Global Variable
path2file = '/home/ubuntu/yelp/aditya'
#user_file = 'yelp_academic_dataset_user.json'
#business_file = 'yelp_academic_dataset_business.json'
#review_file = 'yelp_academic_dataset_review.json'
datatest = "test1.csv"
datatrain = "train1.csv"
reset = True

class MongoDataBase:
	db = None
	def __init__(self, db_name):
		self.db = connect2db.getDb(db_name)

def resetCollection():
	return reset

def deleteAllDocs(db, collection_name):
	db[collection_name].delete_many({})

def convertFile2Collection(db, file_name, collection_name):
	if resetCollection():
		print 'YES'
		deleteAllDocs(db, collection_name)

	f = open(file_name,"r")
	userid_reader = csv.reader(f)
	    #print userid_reader
	userlist = []
        for userid in userid_reader:
                #doc = {}
                #print "jaaaha"
                #doc['_id'] = userid[1]
                #print userid[3]
                #string = userid[2]
                #string = string.replace("\\","")
                #print string
                #doc["business"] = lst[i]
                #i=i+1
                #print doc
		#print userid[1]
		#print userid[2]
		#print userid[3]
	#	int userid
		doc = {}
		doc["userid"] = userid[1]
		doc["friends"] = userid[3]
		doc["business"] = userid[2]
		print doc
		#userlist.append(userid[1])
		db[collection_name].insert(doc)
def main():
	file_arr = [datatest,datatrain]
	mongo_db_obj = MongoDataBase('yelpdb')
	db = mongo_db_obj.db
	test = "test"
	train = "train"
	convertFile2Collection(db,"test10.csv","test10")
	convertFile2Collection(db,"train10.csv","train10")
'''	for i in range(1,10):
		test_file =  test + str(i) + ".csv"
		collection_name = test + str(i)
		train_file = train + str(i)+".csv"
		collectionname = train + str(i)
		convertFile2Collection(db, test_file, collection_name)
		convertFile2Collection(db,train_file, collectionname)'''
	

if __name__ == "__main__" : main() 
