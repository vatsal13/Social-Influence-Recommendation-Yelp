import connect2db
import json
import pymongo

# Global Variable
reset = False
source_collection = 'review'
collection_name = 'items'

class MongoDataBase:
	db = None
	def __init__(self, db_name):
		self.db = connect2db.getDb(db_name)

def resetCollection():
	return reset

def deleteAllDocs(db, collection_name):
	print 'Resetting - ' + collection_name
	db[collection_name].delete_many({})

def populateItems(db):
	if resetCollection():
		deleteAllDocs(db, collection_name)

	review_coll = db[source_collection]
	
	for i in review_coll:
		print i
		break



	pass

def main():
	mongo_db_obj = MongoDataBase('yelpdb')
	db = mongo_db_obj.db
	populateItems(db)

	return None

if __name__ == "__main__" : main() 