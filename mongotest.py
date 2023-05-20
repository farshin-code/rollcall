from dotenv import load_dotenv,find_dotenv
import os
import pprint
from pymongo import MongoClient
import urllib.parse 

load_dotenv(find_dotenv())

password =os.environ.get('MongoDB_pass')
password = urllib.parse.quote_plus(password)
connection_string = f"mongodb+srv://farshinasri:{password}@maincluster.qizxote.mongodb.net/?retryWrites=true&w=majority"
# print(connection_string)
client = MongoClient(connection_string)

dbs = client.list_database_names()
collection = client.local.list_collection_names()
# print(dbs)
# print(collection)

def insert_test_doc():
    dbs = client['Test'] # we can also use client.Test . mongoDB will create that for us
    collection = dbs['Collection_test']
    data = {
        "name" : "farshin",
        "family" : "asri"
    }
    id = collection.insert_one(data).inserted_id
    print(id)

# insert_test_doc()

def create_docs():
    firstNames = ["ali","john","Mcgoal","Special","corner"]
    lastNames = ["asri","babai","sondar","pichai,why"]
    ages=[12,13,45,23,6]
    # first way : 
    # for firstName,lastName,age in zip(firstNames,lastNames,ages):
    #     client.production.persons.insert_one({"firstName":firstName,"lastName":lastName,"age":age})
    # #another way : insert many:
    docs=[]
    for firstName,lastName,age in zip(firstNames,lastNames,ages):
       doc =  {"firstName":firstName,"lastName":lastName,"age":age}
       docs.append(doc)
    client.production.persons.insert_many(docs)
#create_docs()

def get_persons():
    printer = pprint.PrettyPrinter()
    persons = client.production.persons.find()

    for person in persons:
        printer.pprint(person)

#get_persons()

def find_person(name):
    result=  client.production.persons.find_one({"firstName":name})
    print(result)

#find_person("ali")

def count_people():
    result = client.production.persons.count_documents(filter={})
    print(result)

#count_people()

def get_person_by_ID(id):
    from bson.objectid import ObjectId
    _id = ObjectId(id)
    result = client.production.persons.find_one({"_id":_id})
    print(result)


#get_person_by_ID('6447e9fef54690641f1ff31d')


def get_age_range(min_age,max_age):
    query = {"$and":[
            {"age" : {"$gte":min_age}},
            {"age" : {"$lte":max_age}}
        ]}
    
    result = client.production.persons.find(query)
    for person in result:
        pprint.PrettyPrinter().pprint(person)

#get_age_range(6,25)


def project_columns(): # see just few cols
    cols = {"_id":0,"firstName":1,"lastName":1} # i dont mention age here , and it will not be shown!!!! like _id
    people  = client.production.persons.find({},cols)
    for person in people:
        print(person)

#project_columns()

def update_by_ID(id):
    from bson.objectid import ObjectId
    _id=ObjectId(id)

    update = {
        "$set":{"new_field":True}, # if we set the field that does not exist , mongoDB first will create that!
        "$inc":{"age":1},
        "$rename" : {"firstName":"First_Name","lastName":"Last_name"}
    }
    client.production.persons.update_one({"_id":_id},update)

#update_by_ID('6447e9fef54690641f1ff31d')

# delete Field :
#client.production.persons.update_one({"_id":_id},{"$unset":{"new_field":""}})# we used "" because dic in python could have just 1 part
#replace doc:
#client.production.persons.replace_one({"_id":_id},new_doc)
#delete :
#client.production.persons.delete_one({"_id":_id})
#delete many:
# client.production.persons.delete_many({}) # all
# client.production.persons.delete_many(query)

# how to relate fields or add docs for example Address to persons:
address = {
    "Address Line 1" : "127 Stave Cres",
    "Address Line 2" : "",
    "City" : "Richmond Hill",
}

# first way :
## Add it as sub doc , but because person can have more than 1 address ,we will add it as 1 element of the list of addresses
def first_way():
    from bson.objectid import ObjectId
    client.production.persons.update_one({"_id":ObjectId('6447e9fef54690641f1ff31d')},{"$addToSet":{"addresses" : address}}) # addToSet because it will be list

# second way :
## create another collection for addresses and add field for storing the ID of owner!
def second_way():
    from bson.objectid import ObjectId
    global address
    adrs = address.copy() # just not to change the original one,it is not something that's necessary to do
    adrs["owner_id"] = ObjectId('6447e9fef54690641f1ff31e')
    client.production.addresses.insert_one(adrs)


#first_way()
second_way()