import MySQLdb
import math
import datetime
today    =  datetime.date.today()
db  = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer_funnel')
cursor = db.cursor()
sql = "select * from funnel_customer where 1"
cursor.execute(sql)
customer = cursor.fetchall()
for n in customer:
    cid = n[0]
    lastvisit = n[14]
    diff     = abs(today-lastvisit).days 
    if diff < 180:
        status = 1
    elif diff >180 and diff < 365:
        status = 2
    else:
        status = 3
    sql1 = "update funnel_customer set status = '%s' where id = '%s'" %(status,cid)            
    cursor.execute(sql1)
    db.commit()
    print cid