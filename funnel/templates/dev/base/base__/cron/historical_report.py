import MySQLdb
import math
from geocode import geocode
from datetime import datetime
import hashlib
import time
from common import *
class hreport:
    def __init__(self,db,cursor,data,type):
        self.db            = db
        self.cursor        = cursor
        self.data          = data
        self.type          = type
    def process(self):
        entrydate          = unicode(self.data['entrydate'])
        sp                 = entrydate.split('-')
        year               = int(sp[0])
        month              = int(sp[1])
        dealer             = self.data['dealer']
        sql = "select * from funnel_historical_report where year='%s' and month='%s' and type='%s' and fdealer_id='%s' limit 1" % (year,month,self.type,dealer) 
        self.cursor.execute(sql)
        if self.cursor.rowcount == 0:
            dict = {
                     "year"       :year,
                     "month"      :month,
                     "sales"      :self.data['sales'],
                     "service"    :self.data['service'],
                     "type"       :self.type,
                     "revenue"    :self.data['revenue'],
                     "fdealer_id" : dealer,
                     
                    }
            common().insert('funnel_historical_report',dict,self.cursor,self.db)
        else:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            id     = result[0]
            dict = {
                     "revenue"    : result[common().getindex('funnel_historical_report','revenue', self.cursor)] + self.data['revenue'],
                     "sales"      : result[common().getindex('funnel_historical_report','sales', self.cursor)] + self.data['sales'],                
                     "service"    : result[common().getindex('funnel_historical_report','service', self.cursor)] + self.data['service'],
                    }
            common().update('funnel_historical_report',dict,id,'id',self.cursor,self.db)            