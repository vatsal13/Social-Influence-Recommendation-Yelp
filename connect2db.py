import pymongo
from pymongo import MongoClient

def getDb(db_name):
	client = MongoClient()
	#client = MongoClient('ec2-35-161-96-23.us-west-2.compute.amazonaws.com', 27017)
	client = MongoClient('localhost', 27017)
	db = client[db_name]
	return db