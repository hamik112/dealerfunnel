import MySQLdb
from geocode import *
from common import *
class mapzip:
    def __init__(self,code,db = None, cursor = None):
        if db is None:
            self.db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer_funnel')
            self.cursor = self.db.cursor()
        else:
            self.db     = db
            self.cursor = cursor    
        self.code  = code    
    def setZip(self):
        sql  = "select * from funnel_zipcode where code='%s' limit 1" % self.code
        self.cursor.execute(sql)
        if self.cursor.rowcount == 0:
           lat = geocode(self.code).getlatlng()  
           dict = {"code":self.code,"lat":lat[0],"lng":lat[1]}
           return common().insert('funnel_zipcode', dict,self.cursor,self.db)
        else:
           sql  = "select * from funnel_zipcode where code='%s' limit 1" % self.code
           self.cursor.execute(sql)
           result = self.cursor.fetchone()
           return result[0]