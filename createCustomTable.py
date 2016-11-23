# m.py
import json

hasharr = []
path2file = '/home/ubuntu/yelp/yelp_academic_dataset_review.json'
#path2file = '/home/peps/socialcommerce/review.json'

def set_global(count):
    global doc_count    # Needed to modify global copy of doc_count
    global limit_count    # Needed to modify global copy of limit_count
    doc_count = count
    limit_count = 3;

def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.yelpdb
    return db

if __name__ == "__main__":

    db = get_db()

    #fetch selected number of docs to work on them specifically
    file = path2file
    #print file
    counter = 0;
    with open(file) as f:
        #print 'opened'
        for line in f:
            review = json.loads(line)
            #fetch reviews of this user
            counter+=1
            if counter%10000==0:
                print 'read reviews ', counter
            ratingarr = []
            rating = {}
            found = False
            #print review

            userid = review['user_id']
            #print userid
            business_id = review['business_id']
            #print business_id
            stars = review['stars']
            #print stars
            rating['stars'] = stars;
            rating['business_id'] = business_id
            #print rating
            ratingarr.append(rating)
            #query = {}
            #query['user_id'] = userid
            search_res = db.user_review.find_one({'user_id':userid})
            if search_res and search_res !={}:
                #if userjson['user_id'] == userid:

                val = search_res['reviews']
                val.append(rating)
                #print val

                db.user_review.update_one({'user_id':userid}, {'$set':{'reviews': val}});

            else:
                res_json = {}
                res_json['user_id'] = userid
                res_json['reviews'] = ratingarr
                db.user_review.insert_one(res_json)
