import calendar
import hashlib
from geocode import geocode
import time
from common import *
from datetime import date, timedelta as td
db            = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
cursor        = db.cursor()
dealerid      = 3
# get Data from Cron
sql           = "select * from funnel_outofmarkercron limit 1"
cursor.execute(sql)
if cursor.rowcount == 1:
    results  = cursor.fetchone()
    id       = results[0]
    dealerid = results[1]
    sql      = "delete from funnel_outofmarkercron where id=%s" % id
    cursor.execute(sql)
    db.commit()   
    # get Dealer Market Distance
    sql           = "select * from funnel_dealer where id= %s" % dealerid
    cursor.execute(sql)
    results = cursor.fetchone()
    distance = results[54]
    sql           = "select * from funnel_customer where fdealer_id = %s" % dealerid
    cursor.execute(sql)
    result = cursor.fetchall()
    for n in result:
        id  = n[0]
        dst = n[14]
        if  dst == -1 or dst > distance:
            updatesql = "UPDATE funnel_customer set ismarketout = 1 where id=%s" % id
            cursor.execute(updatesql)
            db.commit()    

print 'Done'
