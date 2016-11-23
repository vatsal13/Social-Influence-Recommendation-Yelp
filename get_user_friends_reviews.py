# m.py
import json

doc_count = 0
limit_count = 0
path2file = '/home/ubuntu/yelp/yelp_academic_dataset_user.json'
#path2file = '/home/peps/socialcommerce/user.json'

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

def get_users(db, x, userid):
    if not userid:
        if x+limit_count > doc_count:
            ef_count = doc_count
        else:
            ef_count = x+limit_count
        return db.user.find({})[x:ef_count]
    else:
        return db.user.find_one({"_id":userid})


def fetch_user_reviews(db, userid):
    #print 'fetching review for user -->',userid
    return list(db.user_review.find({"user_id":userid}))

def get_review_array_from_json(review_json):
    #print 'review_json---->', review_json
    review_arr = []
    ratings = review_json[0]['reviews']
    #print 'ratings---->',ratings
    for rating in ratings:
        temp_json = {}
        temp_json['stars'] = rating['stars']
        temp_json['business_id'] = rating['business_id']
        review_arr.append(temp_json)

    #print 'review_arr---->', review_arr
    return review_arr


def get_user_reviews(db, userid):
    #return fetch_user_reviews(db, userid)
    reviews_json =  fetch_user_reviews(db, userid)
    #return reviews_json
    return get_review_array_from_json(reviews_json);

def compare_reviews(user_reviews, friend_reviews):
    user_reviews_arr = []
    friend_reviews_arr = []
    #extract business ids list from array of json into user_reviews_arr
    for review_json in user_reviews:
        user_reviews_arr.append(review_json['business_id'])
    #extract business ids list from array of json into friend_reviews_arr
    for review_json in friend_reviews:
        friend_reviews_arr.append(review_json['business_id'])

    result = set.intersection(set(user_reviews_arr), set(friend_reviews_arr))
    #print result
    #print len(result)
    if len(result) >= 3:
        return True
    else:
        return False

def remove_friends(user_friends, exclude_friends):
    return list(set(user_friends)-set(exclude_friends))


def insert_in_DB(db, userid, user_reviews, user_friends):
    insertjson = {}
    insertjson['user_id'] = userid
    insertjson['business'] = user_reviews
    insertjson['friends'] = user_friends
    #print 'insert json for user id ', userid, '-->', insertjson
    db.userCustom.insert_one(insertjson)


def get_user_count(db):
    return db.user.count();

if __name__ == "__main__":

    db = get_db()
    counter=0
    #fetch selected number of docs to work on them specifically
    file = path2file
    #print file
    with open(file) as f:
        #print 'opened'
        for line in f:
            counter+=1
            if counter%10000==0:
                print 'processing user id ---->',counter
            user = json.loads(line)
            #fetch reviews of this user
            #fetch reviews of this user
            user_reviews = []
            exclude_friends = []
            #print user
            user_reviews = get_user_reviews(db, user['user_id'])

            #for review in user_reviews:
            #    print review
            #iterate over friends of user and fetch their reviews
            for friend in user['friends']:
                #fetch reviews of this user
                friend_reviews = []
                #print friend
                friend_reviews = get_user_reviews(db, friend)
                #for review in friend_reviews:
                #    print review
                comparison_res = compare_reviews(user_reviews, friend_reviews)
                if not comparison_res:
                    exclude_friends.append(friend)

            #print 'excluded friends for user', user['_id']
            #for exclude_friend in exclude_friends:
            #    print exclude_friend

            #insert json in DB
            ef_friends = remove_friends(user['friends'], exclude_friends)
            insert_in_DB(db, user['user_id'], user_reviews, ef_friends)
