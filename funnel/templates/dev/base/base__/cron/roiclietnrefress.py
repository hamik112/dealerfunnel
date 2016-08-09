import MySQLdb
import math
from geocode import geocode
from datetime import datetime
import hashlib
import time
from common import *
db  = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
cursor = db.cursor()
sql = "update funnel_roiclient set flag = '0'"
cursor.execute(sql)
db.commit()
sql = "update funnel_roiclient set flag = '0'"
cursor.execute(sql)
db.commit()
sql = "update funnel_cron set nconnection = '0' where id='1'"
cursor.execute(sql)
db.commit()