import MySQLdb
import math
from geocode import geocode
from datetime import datetime,timedelta
import hashlib
import time
from common import *
class customer_tradein:
    def __init__(self,db,cursor,raw,customerid):
        self.db            = db
        self.cursor        = cursor
        self.raw           = raw
        self.customerid           = customerid
    
    def process(self):
        if self.raw['tradeins'] == 1:
            csales = self.raw['id']
            year  = self.raw['tradein_1_year']
            make  = self.raw['tradein_1_make']
            model  = self.raw['tradein_1_model']
            mileage  = self.raw['tradein_1_mileage']
            customer_number = self.raw['number']
            dealerid  = self.raw['dealer'] 
            trade_entrydate = self.raw['entrydate']
            sql = "select * from funnel_raw_sales where entrydate<'%s' and vehicleyear='%s' and vehiclemake='%s' and customernumber='%s' and dealerid='%s' limit 1" %(trade_entrydate,year,make,customer_number,dealerid)    
            
            self.cursor.execute(sql)
            if self.cursor.rowcount == 1:
               result  = self.cursor.fetchone()
               p_entrydate = result[common().getindex('funnel_raw_sales','entrydate',self.cursor)]
               psales = result[0]
               dict   = {}
               dict["year"] = year
               dict["make"] = make
               dict["model"] = model
               dict["mileage"] = mileage
               dict["sold_date"] = trade_entrydate
               dict["csales"] = csales
               dict["psales"] = psales
               dict["customerid"] = self.customerid
               dict["dealerid"] = dealerid
               common().insert('funnel_customer_tradein', dict,self.cursor,self.db)
               dict = {}
               dict["istradecycle"] = 1
               common().update('funnel_customer',dict,self.customerid,'id',self.cursor,self.db)
                                    