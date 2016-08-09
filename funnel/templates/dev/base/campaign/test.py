import MySQLdb
import hashlib
from common import *
from loadlead import *
from customer_analysis import *
import datetime
import sys, os
import datetime
now = datetime.datetime.now()
db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer_funnel')
cursor = db.cursor()
sql = "select * from funnel_cron_flag where id = 1"
cursor.execute(sql)
res = cursor.fetchone()
ptime = res[7]
print now
c = now - ptime
print divmod(c.days * 86400 + c.seconds, 60)[0]