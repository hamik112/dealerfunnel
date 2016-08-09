import MySQLdb
import math
from geocode import geocode
from datetime import datetime
import hashlib
import time
from common import *
class topvehicle:
    def __init__(self,db,cursor,data):
        self.db            = db
        self.cursor        = cursor
        self.data          = data
    def process(self):
        if self.data['tradeins'] == 1:
            make   = self.data['make']
            model  = self.data['model']
            dealer = self.data['dealer']
            sql = "select * from funnel_topvehicle where make='%s' and model = '%s' and fdealer_id = '%s' limit 1" % (make,model,self.data['dealer'])    
            self.cursor.execute(sql)
            if self.cursor.rowcount == 0:
               dict = {
                     "make"       : make,
                     "model"      : model,
                     "count"      : 1,
                     "fdealer_id" : dealer,
                     
                    }
               common().insert('funnel_topvehicle',dict,self.cursor,self.db)
            else:
                self.cursor.execute(sql)
                result = self.cursor.fetchone()
                id     = result[0]
                dict = {
                     "count"      : result[common().getindex('funnel_topvehicle','count', self.cursor)] + 1,
                }
                common().update('funnel_topvehicle',dict,id,'id',self.cursor,self.db)
                       