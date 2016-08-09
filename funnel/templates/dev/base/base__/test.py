from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo
from datetime import datetime
import datetime
from dateformate import dateformateclass

client        = MongoClient('localhost:27017')
db            = client.funnel

cid           = 3

# Define Date

end_date      = datetime.datetime.now().date()
start_date    = end_date-datetime.timedelta(6)

stringStartDate = dateformateclass().strday(start_date.strftime('%d')) + ' ' + start_date.strftime('%b') + ' ' + start_date.strftime('%y')
stringEndDat= dateformateclass().strday(end_date.strftime('%d')) + ' ' + end_date.strftime('%b') + ' ' + end_date.strftime('%y')

#Calculate Date Sequence
 
date_sequence = dateformateclass().date_sequence(start_date,end_date)[1]
str_date      = []
str_date.append("")
for n in date_sequence:
    str_date.append(n)

# Calculate Respone
web           = []
phone         = []
app           = []
for n in range(0,7):
    web_count     = 0
    phone_count   = 0
    app_count     = 0
    temp_date     = end_date - datetime.timedelta(6-n)
    enddatetime   = datetime.datetime(temp_date.year,temp_date.month,temp_date.day,0,1)  
    startdatetime = datetime.datetime(temp_date.year,temp_date.month,temp_date.day,23,59)
    match        = {"campaign":cid,"date":{"$gte":enddatetime,"$lte":startdatetime}}
    data         = db.leadresponse.aggregate([{"$match":match},{"$group":{"_id":"$responsetype","count":{"$sum":1}}}])
    doc          = list(data)
    if len(doc)  == 0:
        app.append([n+1,0])
        web.append([n+1,0])
        phone.append([n+1,0])
    else:
        for k in doc:
            if  k['_id'] == 1 or k['_id'] == 2:
                phone_count = phone_count + k['count']
            if  k['_id'] == 3:
                web_count = k['count']
            if  k['_id'] == 4:
                app_count = k['count']
        app.append([n+1,app_count])
        web.append([n+1,web_count])
        phone.append([n+1,phone_count])                    
jsonData        = {}
jsonData['app'] = app
jsonData['phone'] = phone
jsonData['web'] = web
jsonData['sequence'] = str_date
jsonData['strdate'] = [stringStartDate,stringEndDat]
print jsonData


    