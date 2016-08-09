import datetime
import random
from bson.objectid import ObjectId
def getDate():
    day   = int(random.randint(1,28))
    month = int(random.randint(1,12))
    year  = int(random.randint(2010,2015))
    hour  = int(random.randint(1,23))
    min   = int(random.randint(0,59))
    sec   = int(30)
    return datetime.datetime(year,month,day,hour,min)
def getTag():
    lst = ['Good','Bad','Odd','Cool','Fine','Ok','Worker','Lessi','Luky']
    return lst[random.randint(0,8)]
def getCity():
    lst = ['Ullapara','Dhaka','Nator','Pabna','Bogra','Rajshahi','Khulna','Chitagong','Shavar']
    return lst[random.randint(0,8)]
def getTitle():
    lst = ['Student','Doctor','Lawer','Engineer','Teacher','Bangker','Bussiness','Govment','Consultant']
    return lst[random.randint(0,8)]
def get_db():
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client.funnel
    return db
def postLead(db):
    db.lead.insert({"name":"khalid"})

now = datetime.datetime.now()

db = get_db()

for n in range(0,10000):
    dict = {}
    dict['tag'] = getTag()
    dict['title'] = getTitle()
    dict['city'] = getCity()
    dict['date'] = getDate()
    dict['age'] = random.randint(20,55)
    dict['salary'] = random.randint(20000,400000)
    db.leadtest.insert_one(dict)
print 'Done'
