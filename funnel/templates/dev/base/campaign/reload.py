import MySQLdb
from common import *
from geocode import *
db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer')
cursor = db.cursor()
sql = "UPDATE `sale` SET processed_flag=0 WHERE 1"
cursor.execute(sql)
db.commit()
sql = "UPDATE `service` SET processed_flag=0 WHERE  1"
cursor.execute(sql)
db.commit() 
cursor.close()
db.close() 
db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer_funnel')
cursor = db.cursor()
sql = "UPDATE `funnel_cron_flag` SET status=0 WHERE 1"
cursor.execute(sql)
db.commit()

sql = "delete from  `funnel_customer_roi`  WHERE 1 "
cursor.execute(sql)
db.commit()

sql = "delete from  `funnel_topzipcode`  WHERE 1"
cursor.execute(sql)
db.commit()

sql = "delete from  `funnel_topvehicle`  WHERE 1"
cursor.execute(sql)
db.commit()

sql = "delete from  `funnel_historical_report`  WHERE 1 "
cursor.execute(sql)
db.commit()

sql = "delete from  `funnel_customer`  WHERE 1 "
cursor.execute(sql)
db.commit()


'''
sql = "delete from  `funnel_lead_expiredata`  WHERE 1"
cursor.execute(sql)
db.commit()
sql = "delete from  `funnel_lead`  WHERE 1"
cursor.execute(sql)
db.commit()
sql = "delete from  `funnel_topzipcode`  WHERE 1"
cursor.execute(sql)
db.commit()
sql = "delete from  `funnel_topvehicle`  WHERE 1"
cursor.execute(sql)
db.commit()
'''
cursor.close()
db.close()