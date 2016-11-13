import connect2db
import json
import pymongo

# Global Variable
path2file = '/home/ubuntu/yelp'
user_file = 'yelp_academic_dataset_user.json'
business_file = 'yelp_academic_dataset_business.json'
review_file = 'yelp_academic_dataset_review.json'
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

	file = path2file + file_name

	with open(file) as f:
			for line in f:
				doc = json.loads(line)

				if collection_name == 'user':
					doc['_id'] = doc['user_id']
				elif collection_name == 'business':
					doc['_id'] = doc['business_id']
				elif collection_name == 'review':
					doc['_id'] = doc['review_id']

				db[collection_name].insert(doc)

def main():
	file_arr = [review_file, business_file, user_file]
	mongo_db_obj = MongoDataBase('yelpdb')
	db = mongo_db_obj.db

	for file in file_arr:
		collection_name = file.split('_')[-1].split('.')[0]
		convertFile2Collection(db, file, collection_name)
	
	return None

if __name__ == "__main__" : main() 