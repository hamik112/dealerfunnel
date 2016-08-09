import MySQLdb
import math
from geocode import geocode
from datetime import datetime
import hashlib
import time
from common import *
db  = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
#db  = MySQLdb.connect('localhost','root','123456','dealerfunnel')
cursor = db.cursor()
sql= "select * from funnel_raw_sales where dealerid='7' and  tradein_1_vin!=''"
cursor.execute(sql)
results = cursor.fetchall()
i = 0
s = 0
for n in results:
    s = s + 1  
    vin = n[common().getindex('funnel_raw_sales','tradein_1_vin',cursor)]
    entrydate = n[common().getindex('funnel_raw_sales','entrydate',cursor)]
    tradeid = n[0]
    sql1= "select * from funnel_raw_sales where dealerid='7' and  vehiclevin = '%s'" % vin
    cursor.execute(sql1)
    
    if cursor.rowcount > 1:
       result = cursor.fetchone()
       matchentry = result[common().getindex('funnel_raw_sales','entrydate',cursor)]
       matchtradein = result[0]
       i = i + 1
       print "Trade Id:" +  str(tradeid)
       print "Match Id:" +  str(matchtradein)
       print "Match Entry Date:" +  str(matchentry)
       print "Trade Date:" +  str(entrydate)
       print "Match:" +  str(i) + '/' + str(s)
       if matchentry < entrydate:
           print "Yes"
       else:
           print "No"    
       print "======================================================"   