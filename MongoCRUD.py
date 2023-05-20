from dotenv import load_dotenv,find_dotenv
import os
import pprint
from pymongo import MongoClient
from bson.objectid import ObjectId 
from bson.json_util import dumps # convert result to json
from datetime import datetime

# import urllib.parse 
# import certifi
# ca = certifi.where()

load_dotenv(find_dotenv())

# password =os.environ.get('MongoDB_pass')
# password = urllib.parse.quote_plus(password) # because I have @ in my Password
connection_string = f"mongodb://localhost:27017"
client = MongoClient(connection_string)

user_validator = {
    "$jsonSchema" :{
        "bsonType" : "object",
        "required":["name","id","username","password"],
        "properties" : {
            "name" : {
                "bsonType" : "string",
                "description" : "Must be string and not empty!"
            },
            "id" :{
                "bsonType":"int",
                "description" : "Must be number and not empty!"

            },
            "username" :{
                "bsonType":"string",
                "description" : "Must be string and not empty!"
            },
            "password" :{
                "bsonType" : "string",
                "description" :"Must be 8 character and more"
            }

        }
    }
}
sign_validator = {
    "$jsonSchema" :{
        "bsonType" : "object",
        "required":["id","date_time","whoRegistered"],
        "properties" : {
            "id" : {
                "bsonType" : "objectId",
                "description" : "Must be ObjectID and not empty!"
            },
            "date_time" :{
                "bsonType":"date",
                "description" : "Must be date/time and not empty!"
            },
            "whoRegistered" :{
                "bsonType" : "objectId",
                "description" :"Must be 8 character and more"
            }

        }
    }
}



def mongoDB_init():
    db = client["rollcall"]

    if "users"  not in db.list_collection_names():
        print("'users' collection is not exist so I will create that")
        db.create_collection("users",validator = user_validator)
        # we can also send command to add validator like this :
        #db.command("collMod","users",validator = user_validator)
    else:
        print("'users' collection is already exist")
    if "signs" not in db.list_collection_names():
        print("signs collection is not exist so I will create that")
        db.create_collection("signs",validator = sign_validator)
    else:
        print("signs collection is already exist")

#mongoDB_init()

def IDcheck(id):
    return client.rollcall.users.count_documents({"id":id})
def getIDobjectById(id):
    return client.rollcall.users.find({'id':int(id)})[0]['_id']
def getIDobjectByUser(user):
    return client.rollcall.users.find({'username':user})[0]['_id']

def emailCheck(email):
    return client.rollcall.users.count_documents({"username":email})

def userCheck(id,email):
    IDresult = client.rollcall.users.count_documents({"id":id})
    emailResult = client.rollcall.users.count_documents({"username":email})
    
    result=""
    if IDresult:
        result="id"
    if emailResult:
        result="username"
    return result
    
def user_insert(name,id,username,password):
    client.rollcall.users.insert_one({"name":name,"id":id,"username":username,"password":password})

def check_userPass(user,Pass):
     return client.rollcall.users.count_documents({"username":str.strip(user),"password":str.strip(Pass)})

def check_IDPass(ID,Pass):
     return client.rollcall.users.count_documents({"id":int(ID),"password":str.strip(Pass)})

def sign_insert(id,date_time,whoRegistered = None):
    dt = datetime.strptime(date_time,"%H:%M %m/%d/%Y")

    doc = {
        'id': ObjectId(id),
        'date_time':dt,
        'whoRegistered':whoRegistered
    }
    client.rollcall.signs.insert_one(doc)


def query_signs(id,start_date,end_date,page_number):
    start_date = datetime.strptime(start_date,"%H:%M %m/%d/%Y")
    end_date = datetime.strptime(end_date,"%H:%M %m/%d/%Y")

    
    if id != 'ALL':

        #  return_value = client.rollcall.signs.find({"_id":id,"date_time":{"$gte":start_date},"date_time":{"$lte":end_date}}) \
        #     .skip(0 if page_number==1 else page_number*10 ).limit(10)
        return_value = client.rollcall.signs.aggregate([
      
        { '$match':{
            '$and' :[{'date_time':{'$gte':start_date} },{'date_time':{'$lte':end_date}},{"_id":id}]
            }
        },
    
        {
            '$lookup': {
            'from': "users",
            'localField': 'whoRegistered',
            'foreignField':'_id',
            'as': 'registeredBy'
            }
        },
        {
            '$lookup': {
            'from': "users",
            'localField': 'id',
            'foreignField':'_id',
            'as': 'user'
            }

        },
        {
            '$project' : {'date_time':1,'registeredBy.name':1,'user.name':1}
        },
        { 
            '$skip': 0 if page_number==1 else page_number*10 
        },
        { 
            '$limit':10 
        }

        ])

        return dumps(list(return_value))
    
    else:
        # return_value =  client.rollcall.signs.find({"date_time":{"$gte":start_date},"date_time":{"$lte":end_date}}) \
        #     .skip(0 if page_number==1 else page_number*10 ).limit(10)
        return_value = client.rollcall.signs.aggregate([
      
        { '$match':{
            '$and' :[{'date_time':{'$gte':start_date} },{'date_time':{'$lte':end_date}}]
            }
        },
        
        {
            '$lookup': {
            'from': "users",
            'localField': 'whoRegistered',
            'foreignField':'_id',
            'as': 'registeredBy'
            }
        },
        {
            '$lookup': {
            'from': "users",
            'localField': 'id',
            'foreignField':'_id',
            'as': 'user'
            }

        },
        {
            '$project' : {'date_time':1,'registeredBy.name':1,'user.name':1}
        },
        { 
            '$skip': 0 if page_number==1 else page_number*10 
        },
        { 
            '$limit':10 
        }
        

        ])

        return list(return_value)

