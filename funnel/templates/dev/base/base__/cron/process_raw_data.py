import MySQLdb
import math
from geocode import geocode
from datetime import datetime
import hashlib
import time  
from common import *
class getrawdata:
    def __init__(self,db,cursor,raw,type):
        self.db            = db
        self.cursor        = cursor
        self.raw           = raw
        self.type          = type
        self.raw_table     = ['','funnel_raw_sales','funnel_raw_service'] 
    def get_zip(self,zip):
        list = zip.split('-')
        return list[0][:5]
    def fixdateissue(self,date):
        
        if date is None:
            return '0000-00-00'
        else:
            return date
    def getname(self,fname,lname,name):
        namelist      = [self.fixstringissue(fname),self.fixstringissue(lname)]
        if fname == '':
            n     = name.split(' ')
            slen  = len(n)
            if slen>=2:
                namelist[0] = self.fixstringissue(n[0])
                namelist[1] = self.fixstringissue(n[slen-1])
        return namelist
    def removestringissue(self,val):
        return val.replace("'","")
    def fixstringissue(self,val):
        return val.replace("'","\\'")
    def getzipcode(self,zip):
        sql = "select * from funnel_zipcode where code= '%s' limit 1" % zip
        self.cursor.execute(sql)
        if self.cursor.rowcount == 0:
            geo          = geocode(zip)
            latlng       = geo.getlatlng()
            dict         = {}
            dict['lat']  = latlng[0]
            dict['lng']  = latlng[1]
            dict['code'] = zip
            return common().insert('funnel_zipcode',dict,self.cursor,self.db)
        else:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            return result[0]     
    def distance(self,zip,dealerid):
        sql      = "select * from funnel_dealer where id='%s' limit 1" % dealerid
        self.cursor.execute(sql)
        result   = self.cursor.fetchone()
        dzip     = result[common().getindex('funnel_dealer','fzip_id',self.cursor)]
        sql      = "select * from funnel_zipcode where id= '%s' limit 1" % dzip
        self.cursor.execute(sql)
        result1  = self.cursor.fetchone()
        dzipcode = result1[common().getindex('funnel_zipcode','code',self.cursor)]
        sql      = "select * from funnel_zipcode_distance where zip1='%s' and zip2='%s' limit 1" %(dzipcode,zip)
        self.cursor.execute(sql)
        if self.cursor.rowcount == 0:
            distance  = geocode(dzipcode,zip).distance()
            dict      = {"zip1":dzipcode,"zip2":zip,"val":distance}
            common().insert('funnel_zipcode_distance', dict, self.cursor,self.db)
            return distance
        else:
            self.cursor.execute(sql)
            result  = self.cursor.fetchone()
            return  result[common().getindex('funnel_zipcode_distance','val',self.cursor)]      
    def process(self):
        name                   = self.getname(self.raw[common().getindex(self.raw_table[self.type],'customerfirstname',self.cursor)],self.raw[common().getindex(self.raw_table[self.type],'customerlastname',self.cursor)],self.raw[common().getindex(self.raw_table[self.type],'customername',self.cursor)])
        dict                   = {}
        dict['id']             = self.raw[0]
        dict['email']          = self.removestringissue(self.raw[common().getindex(self.raw_table[self.type],'customeremail',self.cursor)])
        dict['dealer']         = self.raw[common().getindex(self.raw_table[self.type],'dealerid',self.cursor)]
        self.dealer            = dict['dealer']
        dict['number']         = self.raw[common().getindex(self.raw_table[self.type],'customernumber',self.cursor)]
        dict['fname']          = name[0]
        dict['lname']          = name[1]
        dict['address']        = self.removestringissue(self.raw[common().getindex(self.raw_table[self.type],'customeraddress',self.cursor)])
        dict['city']           = self.raw[common().getindex(self.raw_table[self.type],'customercity',self.cursor)]
        dict['state']          = self.raw[common().getindex(self.raw_table[self.type],'customerstate',self.cursor)]
        dict['zip']            = self.get_zip(self.raw[common().getindex(self.raw_table[self.type],'customerzip',self.cursor)])
        dict['zipid']          = self.getzipcode(dict['zip'])
        dict['homephone']      = self.raw[common().getindex(self.raw_table[self.type],'customerhomephone',self.cursor)]
        dict['workphone']      = self.raw[common().getindex(self.raw_table[self.type],'customerworkphone',self.cursor)]
        dict['cellphone']      = self.raw[common().getindex(self.raw_table[self.type],'customercellphone',self.cursor)]
        dict['frontgross']     = 0
        dict['birthdate']      = self.fixdateissue(self.raw[common().getindex(self.raw_table[self.type],'customerbirthdate',self.cursor)])
        dict['backgross']      = 0
        dict['cashprice']      = 0
        dict['roamount']       = 0
        dict['distance']       = self.distance(dict['zip'],self.dealer)
        dict['dealer']         = self.dealer
        dict['sales']          = 0
        dict['service']        = 0
        dict['type']           = self.type
        dict['tradeins']       = 0
        dict['revenue']        = 0
        if self.type == 1:
            dict['sales']      = 1
            tradeins           =  self.raw[common().getindex(self.raw_table[self.type],'TradeIn_1_VIN',self.cursor)]
            if tradeins == "":
               dict['tradeins']= 0
            else:
               dict['tradeins']= 1     
            dict['entrydate']  =  self.raw[common().getindex(self.raw_table[self.type],'entrydate',self.cursor)]
            dict['frontgross'] =  self.raw[common().getindex(self.raw_table[self.type],'frontgross',self.cursor)]
            dict['backgross']  =  self.raw[common().getindex(self.raw_table[self.type],'backgross',self.cursor)]
            dict['cashprice']  =  self.raw[common().getindex(self.raw_table[self.type],'cashprice',self.cursor)]
            dict['revenue']    =  dict['cashprice']
            dict['leasefirstpaydate']    =  self.raw[common().getindex(self.raw_table[self.type],'leasefirstpaydate',self.cursor)]
            dict['leaseterm']  =  self.raw[common().getindex(self.raw_table[self.type],'leaseterm',self.cursor)]
            dict['vehiclevin']  =  self.raw[common().getindex(self.raw_table[self.type],'vehiclevin',self.cursor)]
            dict['vehiclemileage']  =  self.raw[common().getindex(self.raw_table[self.type],'vehiclemileage',self.cursor)]
            dict['tradein_1_vin']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_1_vin',self.cursor)]
            dict['tradein_2_vin']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_2_vin',self.cursor)]
            dict['tradein_1_make']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_1_make',self.cursor)]
            dict['tradein_2_make']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_2_make',self.cursor)]
            dict['tradein_1_model']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_1_model',self.cursor)]
            dict['tradein_2_model']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_2_model',self.cursor)]
            dict['tradein_1_year']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_1_year',self.cursor)]
            dict['tradein_2_year']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_2_year',self.cursor)]
            dict['tradein_1_mileage']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_1_mileage',self.cursor)]
            dict['tradein_2_mileage']  =  self.raw[common().getindex(self.raw_table[self.type],'tradein_2_year',self.cursor)]
            if dict['leaseterm'] == '':
               dict['leaseterm'] = 0 
            dict['extendedwarrantyterm'] = self.raw[common().getindex(self.raw_table[self.type],'extendedwarrantyterm',self.cursor)]
        else:
            dict['vehiclemileage']  =  self.raw[common().getindex(self.raw_table[self.type],'vehiclemileage',self.cursor)]
            dict['service']    = 1
            dict['entrydate']  =  self.raw[common().getindex(self.raw_table[self.type],'closeddate',self.cursor)]
            dict['roamount']   =  self.raw[common().getindex(self.raw_table[self.type],'roamount',self.cursor)]
            dict['revenue']    =  dict['roamount']
            dict['warrantyexpirationdate']  =  self.raw[common().getindex(self.raw_table[self.type],'warrantyexpirationdate',self.cursor)]
        dict['year']           =  self.raw[common().getindex(self.raw_table[self.type],'vehicleyear',self.cursor)]
        dict['make']           =  self.raw[common().getindex(self.raw_table[self.type],'vehiclemake',self.cursor)]
        dict['model']          =  self.raw[common().getindex(self.raw_table[self.type],'vehiclemodel',self.cursor)]
        dict['model']          =  self.raw[common().getindex(self.raw_table[self.type],'vehiclemodel',self.cursor)]        
        return dict                                     