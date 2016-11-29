import json
import pymongo
import connect2db
from math import sqrt
import csv

f2 = open("average_cf.txt","a+")
f3 = open("average_fa.txt","a+")
class MongoDataBase:
        db = None
        def __init__(self, db_name):
                self.db = connect2db.getDb(db_name)
def accuracy_c(db,collection_name,f,j):
	f1 = open(f,"r")
	i=0
	sum=0
	for line in f1:
		i+=1 
		lst = line.split(" ")
		string1 = lst[0]
		ratings = (lst[1])
		string2 = lst[2]
		s = string2[0:22]	
		#print lst
		find = db[collection_name].find({"userid":string1,"business.business_id":s})
		for loop in find:
			string3 = int(loop["business"]["stars"])	
			print ratings, string3
			diff = float(ratings) - string3
			square = pow(diff,2)
			sum+=square
	print sum
	error = sqrt(sum/i)
	print error
	if j==0:
		f2.write(str(error))
		f2.write("\n")
	else:
		f3.write(str(error))
		f3.write("\n")
		
			
		
def main():
        mongo_db_obj = MongoDataBase('yelpdb')
        db = mongo_db_obj.db
	file = ["cf.txt","fa.txt"]
	accuracy_c(db,"test10","cf10.txt",0)
	accuracy_c(db,"test10","fa_10.txt",1)
	'''for i in range(1,11):
		f = "cf"+str(i)+".txt"
		collection = "text"+str(i)
	        accuracy_c(db,collection,f,0)
		f1 = "fa_"+str(i)+".txt"
                accuracy_c(db,collection,f1,1)'''

if __name__ == "__main__" : main()

