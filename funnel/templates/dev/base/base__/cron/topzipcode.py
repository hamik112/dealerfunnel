import MySQLdb
import math
from geocode import geocode
from datetime import datetime
import hashlib
import time
from common import *
class topzipcode:
    def __init__(self,db,cursor,data):
        self.db            = db
        self.cursor        = cursor
        self.data          = data
    def process(self):
        sql = "select * from funnel_topzipcode where zip='%s' and city='%s' and state = '%s' and fdealer_id = '%s' limit 1" % (self.data['zip'],self.data['city'],self.data['state'],self.data['dealer'])    
        self.cursor.execute(sql)
        if self.cursor.rowcount == 0:
            dict = {
                     "zip"        : self.data['zip'],
                     "city"       : self.data['city'],
                     "state"      : self.data['state'],
                     "count"      : 1,
                     "sales"      : self.data['sales'],
                     "service"    : self.data['service'],
                     "fdealer_id" : self.data['dealer'] 
                    }
            common().insert('funnel_topzipcode',dict,self.cursor,self.db)
        else:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            id     = result[0]
            dict = {
                     "count"      : result[common().getindex('funnel_topzipcode','count', self.cursor)] + 1,
                     "sales"      : result[common().getindex('funnel_topzipcode','sales', self.cursor)] + self.data['sales'],                
                     "service"    : result[common().getindex('funnel_topzipcode','service', self.cursor)] + self.data['service'],
                    }
            common().update('funnel_topzipcode',dict,id,'id',self.cursor,self.db)       