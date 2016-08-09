import MySQLdb
import math
from geocode import geocode
from datetime import datetime,timedelta
import hashlib
import time
from common import *
class customer_roi:
    def __init__(self,db,cursor,raw,customerid):
        self.db            = db
        self.cursor        = cursor
        self.raw           = raw
        self.customerid    = customerid
    
    def addmonth(self,entrydate,month):
        return (entrydate + timedelta(month * 30))
    def calculate_date_diff(self,s1,s2):
        a = datetime.strptime(unicode(s1),"%Y-%m-%d")
        b = datetime.strptime(unicode(s2),"%Y-%m-%d")
        diff  = a - b 
        if diff.days < 0:
            return diff.days * -1
        else:
            return diff.days
    def getdelay(self):
        customerid = self.customerid
        gdata = self.gdata
        if gdata['type'] == 1:
            gdata['service_delay'] = 0
            sql    = "select * from funnel_customer_roi where type='1' and  fcustomer_id='%s' order by entrydate DESC limit 1 " % self.customerid
            self.cursor.execute(sql)
            if self.cursor.rowcount == 0:
                gdata['sales_delay'] = 0
            else:
                result     = result = self.cursor.fetchone()
                rentrydate = result[common().getindex('funnel_customer_roi','entrydate',self.cursor)] 
                gdata['sales_delay'] = self.calculate_date_diff(rentrydate,gdata['entrydate'])
        else:
            sql    = "select * from funnel_customer_roi where type='2' and  fcustomer_id='%s' order by entrydate DESC limit 1 " % self.customerid
            self.cursor.execute(sql)
            gdata['sales_delay'] = 0
            if self.cursor.rowcount == 0:
                gdata['service_delay'] = 0
            else:
                result     = result = self.cursor.fetchone()
                rentrydate = result[common().getindex('funnel_customer_roi','entrydate',self.cursor)] 
                gdata['service_delay'] = self.calculate_date_diff(rentrydate,gdata['entrydate']) 
        sql    = "select * from funnel_customer_roi where fcustomer_id='%s' order by entrydate DESC limit 1 " % self.customerid
        self.cursor.execute(sql)
        if self.cursor.rowcount == 0:
           gdata['delay'] = 0
        else:
           result     = result = self.cursor.fetchone()
           rentrydate = result[common().getindex('funnel_customer_roi','entrydate',self.cursor)] 
           gdata['delay'] = self.calculate_date_diff(rentrydate,gdata['entrydate'])
        self.gdata = gdata
        dict = {}
        if gdata['service_delay'] >= 180:
           dict["islateservice"] = 1
        else :
           dict["islateservice"] = 0
        common().update('funnel_customer',dict,self.customerid,'id',self.cursor,self.db)                      
        
    def gatherdata(self):
        dict = {}
        dict["entrydate"] = self.raw["entrydate"]
        dict["grossprofit"] = self.raw["frontgross"] + self.raw["backgross"]
        dict["carsold"] = self.raw["cashprice"]
        dict["invoiced"] = self.raw["revenue"]
        dict["year"] = self.raw["year"]
        dict["make"] = self.raw["make"]
        dict["model"] = self.raw["model"]
        dict["mileage"] = self.raw["vehiclemileage"]
        dict["leaseexpiration"] = '0000-00-00'
        dict["warrantyexpiration"] = '0000-00-00'
        dict["iswarrantyexpiration"] = 0
        dict["isleaseexpiration"] = 0
        dict["tyear"] = ''
        dict["tmake"] = ''
        dict["tmodel"] = ''
        dict["tmileage"] = ''
        dict["type"] = int(self.raw['type'])
        dict["istradein"] = 0
        if dict["type"] == 1:
            dict["fsales_id"] = self.raw["id"]
            dict["tyear"] = self.raw["tradein_1_year"]
            dict["tmake"] = self.raw["tradein_1_make"]
            dict["tmodel"] = self.raw["tradein_1_model"]
            dict["tmileage"] = self.raw["tradein_1_mileage"]
            if int(self.raw['extendedwarrantyterm']) > 0:
               dict["warrantyexpiration"] = self.addmonth(self.raw['entrydate'],int(self.raw['extendedwarrantyterm']))
               dict["iswarrantyexpiration"] = 1
            if int(self.raw['leaseterm']) > 0:
               dict["leaseexpiration"] = self.addmonth(self.raw['entrydate'],int(self.raw['leaseterm']))
               dict["isleaseexpiration"] = 1  
        else:
            dict["fservice_id"] = self.raw["id"]    
        dict["fcustomer_id"] = self.customerid
        dict["fdealer_id"] = self.raw["dealer"]
        self.gdata = dict
    def wdatecheck(self,date):
        a = datetime.now()
        b = datetime.strptime(unicode(date),"%Y-%m-%d")
       
        if b<a:
            return 1
        else:
            return 0
    def warranty_and_lease(self):
        sql    = "select * from funnel_customer_roi where fcustomer_id='%s'" % self.customerid
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        iswarrantyexpiration = 0
        isleaseexpiration    = 0
        for n in results:
            warrantyexpiration = n[common().getindex('funnel_customer_roi','warrantyexpiration',self.cursor)]
            leaseexpiration    = n[common().getindex('funnel_customer_roi','leaseexpiration',self.cursor)]
            if warrantyexpiration is not None:
               dt = self.wdatecheck(warrantyexpiration)
               if dt == 1:
                    iswarrantyexpiration = 1
            if leaseexpiration is not None:
               dt = self.wdatecheck(leaseexpiration)
               if dt == 1:
                    isleaseexpiration = 1           
            
        dict = {"iswarrantyexpiration":iswarrantyexpiration,"isleaseexpiration":isleaseexpiration}    
        common().update('funnel_customer',dict,self.customerid,'id',self.cursor,self.db)
        
    def checktradein(self):
        if self.raw['tradeins'] == 1:
            tradevin  = self.raw["tradein_1_vin"]
            customer_number = self.raw['number']
            dealerid  = self.raw['dealer'] 
            trade_entrydate = self.raw['entrydate']
            sql = "select * from funnel_raw_sales where entrydate<'%s' and vehiclevin='%s' and customernumber='%s' and dealerid='%s' limit 1" %(trade_entrydate,tradevin,customer_number,dealerid)    
            
            self.cursor.execute(sql)
            if self.cursor.rowcount == 1:
               gdata = self.gdata 
               gdata['istradein'] = 1
               self.gdata = gdata
               dict = {}
               dict["istradecycle"] = 1
               common().update('funnel_customer',dict,self.customerid,'id',self.cursor,self.db)
    def insert(self):
        gdata = self.gdata 
        id = common().insert('funnel_customer_roi',gdata,self.cursor,self.db)
        return id           
    def process(self):
        self.gatherdata()
        self.getdelay()
        self.checktradein()
        id = self.insert()
        self.warranty_and_lease()
        return id
        
                                        