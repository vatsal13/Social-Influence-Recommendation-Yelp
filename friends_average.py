import json
import pymongo
import connect2db
from math import sqrt
import csv
#f = open("friendsaverage.txt","w")
class MongoDataBase:
        db = None
        def __init__(self, db_name):
                self.db = connect2db.getDb(db_name)


def average(db,name,collection_name,cname,i):
	
	file = "fa"+str(i)+".txt"
	f = open(file,"a+")
	both_rated = {}
	businesslist = []
	userid = db[collection_name].find({"userid":name})
        for user in userid:
                businesslist.append(user["business"])
	#print "Person1",name
	friendlist = user["friends"]
	for business in businesslist:
		both_rated = {}
		sum_probability = 0
		k=0
		list1 = []
		businessid = business["business_id"]
	#	print "Business id", businessid
		for friend in friendlist:
			#print "Person1",name
			#print "Business id", businessid
			#print "friend--------->",friend	
			personid = db[cname].find({"userid":friend,"business.business_id":businessid})
			for person in personid:
                                ratings = person["business"]["stars"]
				if name+" "+friend+" "+businessid+" "+str(ratings) not in list1:
					list1.append(name+" "+friend+" "+businessid+" "+str(ratings))
					sum_probability+=ratings
					#print sum_probability
					k+=1
		if k!=0:
			#print list1	
			#print name, businessid
			average = sum_probability/k
			#print "Average-------------------------->",average
			print name, average, businessid
			f.write(name +" "+ str( average) + " "+ businessid)
			f.write("\n")
			

def user_recommendation(db,collection_name,cname,i):

        userid = db[collection_name].distinct("userid")
        #print userid
        namelist = userid
        for name in namelist:
		#print name
                average(db,name,collection_name,cname,i)




def main():
        mongo_db_obj = MongoDataBase('yelpdb')
        db = mongo_db_obj.db
	#user_recommendation(db,"test2","train2")
	for i in range(1,11):
		test =  "test"+str(i)
		train = "train"+str(i)
		user_recommendation(db, test,train,i)

if __name__ == "__main__" : main()

