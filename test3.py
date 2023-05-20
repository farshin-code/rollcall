from pymongo.mongo_client import MongoClient
client = MongoClient("mongodb://localhost:27017")
from bson.json_util import dumps # convert result to json
from MongoCRUD import query_signs

from datetime import datetime
# dt = datetime.strptime('10:24 05/08/2023',"%H:%M %m/%d/%Y")
# print(dt)

start_date = datetime.strptime('10:30 05/05/2023',"%H:%M %m/%d/%Y")
end_date = datetime.strptime('10:30 05/08/2023',"%H:%M %m/%d/%Y")
print(start_date)
print(end_date)
result =  client.rollcall.signs.aggregate([
      
      { '$match':{
          '$and' :[{'date_time':{'$gte':start_date} },{'date_time':{'$lte':end_date}
            }]
        }
       },
   
     {
        '$lookup': {
        'from': "users",
        'localField': 'whoRegistered',
        'foreignField':'_id',
        'as': 'user'
        }
    },
    {
        '$project' : {'date_time':1,'user.name':1,'_id':0}
    }

])

# for r in result:
#     # print(r[2],r[4][1])
#     #print(r['date_time'],r['Name of Agent'][0]['name'])
#     print(r['user'][0]['name'])
# print(dumps(list(result)))

# for i in list(result):
#     print(i['date_time'])

result = query_signs("ALL",'10:30 05/05/2023','10:30 05/09/2023',1)

for i in result:
    print(i['date_time'])
