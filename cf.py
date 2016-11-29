import json
import pymongo
import connect2db
from math import sqrt
import csv

#f1 = open("cf.txt","w")
class MongoDataBase:
	db = None
        def __init__(self, db_name):
                self.db = connect2db.getDb(db_name)
def pearsons_correlation(db,name,collection_name,cname,i):
	
	#print "here"
	totals = {}
        simSums = {}
        rankings_list =[]
	file = "cf"+str(i)+".txt"
	f1 = open(file, "a+")
	#print userid
		#print "peraon1", name
	businesslist = [] 
	userid = db[collection_name].find({"userid":name})
	for user in userid:
		businesslist.append(user["business"])
	userid_train = db[cname].find({"userid":name})
	businesslist_train = []
	for user in userid_train:
		businesslist_train.append(user["business"])
	#print name, businesslist
	both_rated = {}
	person1_preferences_sum = 0
        person2_preferences_sum = 0
        person1_square_preferences_sum = 0
        person2_square_preferences_sum = 0
        product_sum_of_both_users = 0
	person2_businesslist = []
	friendlist = user["friends"]
		#print "person2", friend
	for friend in friendlist:
		#print "person1", name,"person2", friend
		score = {}
		k=0
		for business in businesslist_train:
			businessid = business["business_id"]
			stars = business["stars"]
	#print user["user_id"], friend, businessid
	
			personid = db[cname].find({"userid":friend,"business.business_id":businessid})
		
			for person in personid:
				ratings = person["business"]["stars"]
				#print user["user_id"],businessid, stars
				#print friend, person["business"]["business_id"], ratings
				
				if businessid not in both_rated:
					k=1
					#print user["user_id"],businessid, stars
	                               	#print friend, person["business"]["business_id"], ratings

					both_rated[businessid] = 1
					person1_preferences_sum =  person1_preferences_sum + stars
                         		person2_preferences_sum = person2_preferences_sum + ratings
					person1_square_preferences_sum = pow(stars,2)+person1_square_preferences_sum
                              		person2_square_preferences_sum = pow(ratings,2)+person2_square_preferences_sum
                               		product_sum_of_both_users = product_sum_of_both_users + stars*ratings

		#	print "Person1 sum", person1_preferences_sum, "Person2 sum", person2_preferences_sum
		#	print "Person1 squre", person1_square_preferences_sum, "Person2 square", person2_square_preferences_sum
		#	print "product",product_sum_of_both_users
		#print "person1", name,"person2", friend
		if k==1:
			number_of_ratings =  len(both_rated)
			if number_of_ratings == 0:
               			return 0
       			numerator_value = product_sum_of_both_users - (person1_preferences_sum*person2_preferences_sum/number_of_ratings)
       			#print "Numerotor",numerator_value
			denominator_value = sqrt((person1_square_preferences_sum - pow(person1_preferences_sum,2)/number_of_ratings) * (person2_square_preferences_sum -pow(person2_preferences_sum,2)/number_of_ratings))
			#print "Denominator",denominator_value
		#print name
		#print friend
		
			if denominator_value == 0:
				r = 0
      				#print "Denominator is 0"
    			else:
				r = numerator_value/denominator_value
			if r not in score:
				score[user["userid"]+" "+friend]=r
				#business_list = db[cname].distinct("business", {"user_id":friend})
				#newlist = [item for businesslist if item not in business_list]
				if r>0:
					for business_2 in businesslist:
						simSums.setdefault(business_2["business_id"],0)
						simSums[business_2["business_id"]] +=r
						totals.setdefault(business_2["business_id"],0)
						totals[business_2["business_id"]] += business_2["stars"]*r
					#print totals
					#print simSums
					#print totals
			        	#print "rresilt------------------------------->",score
#	print name, friend	
	rankings = [(total/simSums[item],item) for item,total in totals.items()]
	rankings.sort()	
	rankings.reverse()
	#print "Rankings",rankings
	for h in rankings:
		print name,round( h[0]), h[1]
		f1.write(name+" "+str(round(h[0]))+" "+h[1])
		f1.write("\n")
	recommendation_list = [recommend_item for score, recommend_item in rankings]
	#print recommendation_list			

	#print bsinesslist
				
def user_recommendation(db,collection_name,cname,i):
	
	userid = db[collection_name].distinct("userid")
	#print userid
        namelist = userid
        for name in namelist:
		#print name
		pearsons_correlation(db,name,collection_name,cname,i)
		

	

def main():
        mongo_db_obj = MongoDataBase('yelpdb')
        db = mongo_db_obj.db
	#user_recommendation(db,"test1","train1")
	for i in range(1,11):
		test = "test" + str(i)
		train = "train" + str(i)
		user_recommendation(db, test,train,i)

if __name__ == "__main__" : main()

