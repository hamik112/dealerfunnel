import MySQLdb
import math
from geocode import geocode
from datetime import datetime
import hashlib
import time
from common import *
from process_raw_data import *
from customer import *
from topzipcode import *
from topvehicle import *
from customer_tradein import *
from historical_report import *
from customer_roi import *
from campaign_roi_match import *
db  = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
#db  = MySQLdb.connect('localhost','root','123456','dealerfunnel')
cursor = db.cursor()

time1 = datetime.now()

sql = "select * from funnel_raw_sales where flag1='0' and dealerid!='' order by entrydate ASC limit 500"
cursor.execute(sql)
results = cursor.fetchall()
i = 1
for row in results:
    id = row[0]
    p = getrawdata(db,cursor,row,1).process()
    cid = customer(db,cursor,p,1).process()
    rid = customer_roi(db,cursor,p,cid).process()
    campaign_roi_match(db,cursor,rid,cid).process()
    topzipcode(db,cursor,p).process()
    topvehicle(db,cursor,p).process()
    hreport(db,cursor,p,1).process()
    dict = {"flag1":'1'}
    common().update('funnel_raw_sales',dict,id,'id',cursor,db)
    
sql = "select * from funnel_raw_service where flag1='0' and dealerid!='' and closeddate!='0000-00-00' order by closeddate ASC limit 500"
cursor.execute(sql)
results = cursor.fetchall()
i = 1
for row in results:
    id = row[0]
    p = getrawdata(db,cursor,row,2).process()
    cid = customer(db,cursor,p,2).process()
    rid = customer_roi(db,cursor,p,cid).process()
    campaign_roi_match(db,cursor,rid,cid).process()
    topzipcode(db,cursor,p).process()
    topvehicle(db,cursor,p).process()
    hreport(db,cursor,p,2).process()
    dict = {"flag1":'1'}
    common().update('funnel_raw_service',dict,id,'id',cursor,db)    
    
    

time2 = datetime.now()    
    
print (time2-time1)    