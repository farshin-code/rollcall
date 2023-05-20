from pymongo.mongo_client import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
# import urllib.parse 
# import certifi
# ca = certifi.where()
# import ssl
from MongoCRUD import getIDobjectById

# password = urllib.parse.quote_plus('Adriana@1396')
client = MongoClient("mongodb://localhost:27017")

# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
# dt = datetime.strptime('09:17 05/05/2023',"%H:%M %m/%d/%Y")

# client['rollcall']['signs'].insert_one({'id':ObjectId('6452679108ca38f6a1ab9915'),'date_time':dt,'whoRegistered':ObjectId('6452679108ca38f6a1ab9915') })

#print(dt)
# print(datetime.timestamp())

x = getIDobjectById('2')
print(x)
