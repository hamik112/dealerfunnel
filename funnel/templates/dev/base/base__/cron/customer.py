import MySQLdb
import math
from geocode import geocode
from datetime import datetime,timedelta
import hashlib
import time
from campaign_roi_match import *
from common import *
class customer:
    def __init__(self,db,cursor,raw,type):
        self.db            = db
        self.cursor        = cursor
        self.raw           = raw
        self.type          = type
    def wdatecheck(self,date):
        a = datetime.now()
        b = datetime.strptime(unicode(date),"%Y-%m-%d")
       
        if b>a:
            return 1
        else:
            return 0
    
        
    def getPinnumber(self):
        sql = "select * from funnel_pinmanage where type='1'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        id     = result[0]
        pin    = int(result[2]) + 1
        dict   = {"end":pin} 
        common().update('funnel_pinmanage',dict,id,'id',self.cursor,self.db)
        return pin                        
    def getmedia(self):
        dict   = {"image":'',"link":'',"isavailable":0}
        return common().insert('funnel_customer_media',dict,self.cursor,self.db)
    def insertnew(self):
        data   = self.raw 
        number = self.raw['number']
        dealer = self.raw['dealer']
        dict = {
                    "barcode":self.getPinnumber(),"number":data['number'],"fname":data['fname'],'lname':data['lname'],
                    "address":data['address'],"city":data['city'],'state':data['state'],
                    "fzip_id":data['zipid'],"distance":data['distance'],'status':0,'birth_date':data['birthdate'],
                    "lastvisit":'0000-00-00',"lastnotification":'0000-00-00','notificationcount':0,
                    "visit":'0',"sales":'0','service':'0','grossprofit':0,'invoiced':0,'last_sales_date':'0000-00-00',
                    'last_service_date':'0000-00-00',"carsold":'0','fdealer_id':dealer,'flag1':0,
                    "homephone":data['homephone'],"workphone":data['workphone'],"cellphone":data['cellphone'],
                    "email":data['email'],"iswarrantyexpiration":0,"isemail":0,"isleaseexpiration":0,
                    "isbirthday":0,"isequityposition":0,"istradecycle":0,"islateservice":0,"fmedia_id":self.getmedia(),
                    "issms":0
                }
        return common().insert('funnel_customer', dict, self.cursor, self.db)         
    def calculate_status(self,date):
        a = datetime.now()
        b = datetime.strptime(unicode(date),"%Y-%m-%d")
        delta = a - b
        if delta.days < 181:
            return 1
        elif delta.days > 180 and delta.days < 366:
            return 2
        else:
            return 3
        
        
    def calculate_date_diff(self,s1,s2):
        a = datetime.strptime(unicode(s1),"%Y-%m-%d")
        b = datetime.strptime(unicode(s2),"%Y-%m-%d")
        diff  = a - b 
        if diff.days < 0:
            return diff.days * -1
        else:
            return diff.days
    def addmonth(self,entrydate,month):
        return (entrydate + timedelta(month * 30))
    def getcampaignId(self,entrydate,customerid):
        sql = "select * from funnel_customer_campaign where fcustomer_id='%s'" % customerid
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        campaignid = ''
        for n in results:
            cmpid = n[2]
            sql1  = "select * from funnel_campaign where id='%s' limit 1" % cmpid
            self.cursor.execute(sql1)
            result = self.cursor.fetchone()
            startdate = result[common().getindex('funnel_campaign','startdate',self.cursor)]
            enddate   = result[common().getindex('funnel_campaign','enddate',self.cursor)]
            if entrydate >= startdate and entrydate <= enddate :
               campaignid = cmpid
        return  campaignid       
    def customer_roi(self,cid):
        rowid   = self.raw['id']
        type    = self.type
        if type == 1:
            grossprofit = self.raw['frontgross'] + self.raw['backgross']
            invoiced = 0
            carsold  = self.raw['cashprice']
            sql     = "select * from funnel_customer_roi where fcustomer_id='%s' and fsales_id='%s' limit 1" % (cid,rowid)
            if int(self.raw['extendedwarrantyterm']) > 0:
                warrantyexpiration = self.addmonth(self.raw['entrydate'],int(self.raw['extendedwarrantyterm']))
            else:
                warrantyexpiration = '0000-00-00'
            if int(self.raw['leaseterm']) > 0:
                leaseexpiration = self.addmonth(self.raw['entrydate'],int(self.raw['leaseterm']))
            else:
                leaseexpiration = '0000-00-00'        
        else :
            grossprofit = 0
            invoiced = self.raw['roamount']
            carsold  = 0
            sql     = "select * from funnel_customer_roi where fcustomer_id='%s' and fservice_id='%s' limit 1" % (cid,rowid)
            warrantyexpiration = '0000-00-00'
            leaseexpiration = '0000-00-00' 
            
        self.cursor.execute(sql)
        list = ['','fsales_id','fservice_id']
        if self.cursor.rowcount == 0:
             dict = {
                     "type":self.type,
                     "warrantyexpiration":warrantyexpiration,
                     "leaseexpiration":leaseexpiration,
                     "entrydate":self.raw['entrydate'],
                     "grossprofit":grossprofit,
                     "invoiced":invoiced,
                     "carsold":carsold,  
                     list[self.type]:rowid,
                     'fcustomer_id':cid
                     }
             roi_id = common().insert('funnel_customer_roi',dict,self.cursor,self.db)
             campaign_roi_match(self.db,self.cursor,roi_id,cid).process()
             return True
        else:
             return False        
    def cupdate(self,id,data):
        sql  = "select * from funnel_customer where id = '%s' limit 1" % id
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        idate  = result[common().getindex('funnel_customer','lastvisit',self.cursor)]       
        dict   = {}
        if idate is None:
            dict['lastvisit']   = data['entrydate']
            if self.type == 1:
                   dict['last_sales_date']  = data['entrydate']
            else:
                   dict['last_service_date']= data['entrydate']
        else:
            a                   = datetime.strptime(unicode(data['entrydate']),"%Y-%m-%d")    
            b                   = datetime.strptime(unicode(idate),"%Y-%m-%d")
            if a > b:
               dict['lastvisit']= data['entrydate']
               if self.type == 1:
                   dict['last_sales_date']  = data['entrydate']
               else:
                   dict['last_service_date']= data['entrydate']    
            else:
               dict['lastvisit']= idate
                  
        dict['status']          = self.calculate_status(dict['lastvisit'])
        dict['visit']           = result[common().getindex('funnel_customer','visit',self.cursor)] + 1
        dict['sales']           = result[common().getindex('funnel_customer','sales',self.cursor)] + data['sales']    
        dict['grossprofit']     = result[common().getindex('funnel_customer','grossprofit',self.cursor)] +  data['frontgross'] + data['backgross']
        dict['carsold']         = result[common().getindex('funnel_customer','carsold',self.cursor)]     +  data['cashprice'] 
        dict['service']         = result[common().getindex('funnel_customer','service',self.cursor)] + data['service']
        dict['invoiced']        = result[common().getindex('funnel_customer','invoiced',self.cursor)] + data['roamount']
        dict['keyid']           = hashlib.sha224(str(id)).hexdigest()
        iswarrantyexpiration    = result[common().getindex('funnel_customer','iswarrantyexpiration',self.cursor)] 
        if self.type == 2:
            if iswarrantyexpiration == 0:
                warrantyexpiration = self.raw['warrantyexpirationdate']
                if warrantyexpiration is not None:
                    dict['iswarrantyexpiration'] = 1
        isleaseexpiration       = result[common().getindex('funnel_customer','isleaseexpiration',self.cursor)]              
        if self.type == 1:
            leasefirstpaydate   = self.raw['leasefirstpaydate']    
            if leasefirstpaydate is not None:
                term            = self.raw['leaseterm']
                if term!="":
                    a = datetime.now()
                    b = datetime.strptime(unicode(leasefirstpaydate),"%Y-%m-%d")
                    delta = a - b
                    month = int(delta.days/30)
                    if month>term:
                       dict['isleaseexpiration'] = 1 
        isbirthday             = result[common().getindex('funnel_customer','isbirthday',self.cursor)]
        if isbirthday == 0:
           birth_date          = result[common().getindex('funnel_customer','birth_date',self.cursor)] 
           if  birth_date is not None:
               dict['isbirthday'] = 1 
        email                     = result[common().getindex('funnel_customer','email',self.cursor)]
        isemail                   = result[common().getindex('funnel_customer','isemail',self.cursor)]
        if  isemail == 0:
            if  email is not None:
              dict['isemail'] = 1              
        common().update('funnel_customer',dict,id,'id',self.cursor,self.db)
        
    def updatenewdata(self,id,presult):
        data       = self.raw
        flag       = False
        fname      = presult[common().getindex('funnel_customer','fname',self.cursor)]
        lname      = presult[common().getindex('funnel_customer','lname',self.cursor)]
        email      = presult[common().getindex('funnel_customer','email',self.cursor)]
        address    = presult[common().getindex('funnel_customer','address',self.cursor)]
        city       = presult[common().getindex('funnel_customer','city',self.cursor)]
        state      = presult[common().getindex('funnel_customer','state',self.cursor)]
        homephone  = presult[common().getindex('funnel_customer','homephone',self.cursor)]
        workphone  = presult[common().getindex('funnel_customer','workphone',self.cursor)]
        cellphone  = presult[common().getindex('funnel_customer','cellphone',self.cursor)]
        birth_date = presult[common().getindex('funnel_customer','birth_date',self.cursor)]
        dict = {}
        if unicode(birth_date) == '0000-00-00':
            flag = True
            dict["birth_date"] = data['birthdate']
        if data['fname']!= "" and  fname != data['fname']:
            flag = True
            dict["fname"] = data['fname']
        if data['lname']!="" and lname != data['lname']:
            flag = True
            dict["lname"] = data['lname']
        if data['email']!="" and email != data['email']:
            flag = True
            dict["email"] = data['email']
        if data['address']!="" and address != data['address']:
            flag = True
            dict["address"] = data['address']
        if data['city']!="" and city != data['city']:
            flag = True
            dict["city"] = data['city']
        if data['state']!="" and state != data['state']:
            flag = True
            dict["state"] = data['state']
        if data['homephone']!="" and homephone != data['homephone']:
            flag = True
            dict["homephone"] = data['homephone']
        if data['workphone']!="" and workphone != data['workphone']:
            flag = True
            dict["workphone"] = data['workphone']
        if data['cellphone']!="" and cellphone != data['cellphone']:
            flag = True
            dict["cellphone"] = data['cellphone']
        
        if flag:
            common().update('funnel_customer',dict,id,'id',self.cursor,self.db)                                     
             
    def process(self):
        data   = self.raw 
        number = data['number']
        dealer = data['dealer']
        sql ="select * from funnel_customer where number='%s' and fdealer_id='%s' limit 1" % (number,dealer)
        self.cursor.execute(sql)
        if self.cursor.rowcount == 0:
            id = self.insertnew()
        else:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            id = result[0]
            self.updatenewdata(id,result)
        self.cupdate(id,data)
        #self.customer_roi(id)
        #self.calculatedelay(id)  
        #self.warranty_and_lease(id)
        return id          
                                         