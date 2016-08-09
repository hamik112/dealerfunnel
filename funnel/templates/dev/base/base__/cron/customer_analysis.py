import MySQLdb
import math
from  datetime import timedelta
import calendar
import hashlib
from geocode import geocode
import time
from common import *
class customer_analysis:
    def __init__(self,dealer_id):
        self.db            = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
        self.cursor        = self.db.cursor()
        self.dealer_id     = dealer_id
    def process(self):
        dict = {}
        sql = "select * from funnel_customer where fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['total_customer'] = self.cursor.rowcount
        sql = "select * from funnel_customer where birth_date!='0000-00-00' and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['birthday'] = self.cursor.rowcount
        sdate = datetime.now()
        sql = "select DISTINCT * from funnel_customer_roi where  warrantyexpiration>'%s' and fdealer_id = '%s'  GROUP BY  fcustomer_id" % (unicode(sdate),self.dealer_id)
        
        self.cursor.execute(sql)
        dict['warrantyexpiration'] = self.cursor.rowcount
        sql = "select * from funnel_customer where fdealer_id='%s' and DATEDIFF(NOW(),lastvisit)<=180  and  visit>='1' and visit<='2'" % self.dealer_id
        self.cursor.execute(sql)
        dict['active_12'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where fdealer_id='%s' and and DATEDIFF(NOW(),lastvisit)<=180 and  visit>='3' and visit<='4'" % self.dealer_id
        self.cursor.execute(sql)
        dict['active_34'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where fdealer_id='%s' and and DATEDIFF(NOW(),lastvisit)<=180 and  visit >='5' " % self.dealer_id
        self.cursor.execute(sql)
        dict['active_5'] = self.cursor.rowcount
        dict['active'] = dict['active_12'] + dict['active_34'] + dict['active_5']
        
        sql = "select * from funnel_customer where fdealer_id='%s' and  DATEDIFF(NOW(),lastvisit)>180  and DATEDIFF(NOW(),lastvisit)<=360 and  visit>='1' and visit<='2'" % self.dealer_id
        self.cursor.execute(sql)
        dict['less_12'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where fdealer_id='%s' and DATEDIFF(NOW(),lastvisit)>180  and DATEDIFF(NOW(),lastvisit)<=360 and  visit>='3' and visit<='4'" % self.dealer_id
        self.cursor.execute(sql)
        dict['less_34'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where fdealer_id='%s' and DATEDIFF(NOW(),lastvisit)>180  and DATEDIFF(NOW(),lastvisit)<=360 and  visit >='5' " % self.dealer_id
        self.cursor.execute(sql)
        
        dict['less_5'] = self.cursor.rowcount
        dict['lessactive'] = dict['less_12'] + dict['less_34'] + dict['less_5']
        
        sql = "select * from funnel_customer where fdealer_id='%s' and DATEDIFF(NOW(),lastvisit)>360 and  visit>='1' and visit<='2'" % self.dealer_id
        self.cursor.execute(sql)
        dict['lost_12'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where fdealer_id='%s' and DATEDIFF(NOW(),lastvisit)>360 and  visit>='3' and visit<='4'" % self.dealer_id
        self.cursor.execute(sql)
        dict['lost_34'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where fdealer_id='%s' and DATEDIFF(NOW(),lastvisit)>360 and  visit >='5' " % self.dealer_id
        self.cursor.execute(sql)
        dict['lost_5'] = self.cursor.rowcount
        dict['lost'] = dict['lost_5'] + dict['lost_34'] + dict['lost_12']
        sdate = datetime.now()
        sql = "select DISTINCT * from funnel_customer_roi where  leaseexpiration>'%s'  and fdealer_id = '%s'  GROUP BY  fcustomer_id" % (unicode(sdate),self.dealer_id)
        self.cursor.execute(sql)
        dict['leaseexpiration'] = self.cursor.rowcount
        sdate = datetime.now() - timedelta(730)
        sql = "select DISTINCT * from funnel_customer_roi where  entrydate<='%s' and fdealer_id = '%s'  and istradein='1' GROUP BY  fcustomer_id" % (unicode(sdate),self.dealer_id)
       
        self.cursor.execute(sql)
        dict['tradecycle'] = self.cursor.rowcount
        sdate = datetime.now() - timedelta(180)
        sql = "select  * from funnel_customer where last_service_date <= '%s'  and fdealer_id='%s' " % (sdate,self.dealer_id)
        self.cursor.execute(sql)
        dict['lateservice'] = self.cursor.rowcount
        dict['euityposition']   = 0
        dict['makeconquest']        = 0
        dict['crossoverconquest']   = 0
        sql = "select * from funnel_customer where fdealer_id='%s' order by lastvisit ASC limit 1" % self.dealer_id
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        if results is None:
            dict['lastvisit'] = '0000-00-00'
        else:    
            dict['lastvisit'] = results[common().getindex('funnel_customer','lastvisit',self.cursor)]
        
        sql = "select * from funnel_customer where fdealer_id='%s' order by lastvisit DESC limit 1" % self.dealer_id
        self.cursor.execute(sql)
        results = self.cursor.fetchone()
        if results is None:
            dict['latestvisit'] = '0000-00-00'
        else:
            dict['latestvisit'] = results[common().getindex('funnel_customer','lastvisit',self.cursor)]
        sql = "select * from funnel_customer where  service='0' and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['bns'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where  sales='0' and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['snb'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where  sales>=1 and service>=1 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['bs'] = self.cursor.rowcount
        
        sql = "SELECT * FROM `funnel_customer` WHERE `address` is not null  and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['customer_withaddress'] = self.cursor.rowcount
        
        sql = "SELECT * FROM `funnel_customer` WHERE (`homephone` is not null or `workphone` is not null or `cellphone` is not null)  and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['customer_withphone'] = self.cursor.rowcount
        
        sql = "SELECT * FROM `funnel_customer` WHERE `email` is not null and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['customer_withemail'] = self.cursor.rowcount
        
        sql = "SELECT * FROM `funnel_customer` WHERE `email` is not null and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['customer_withemail'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where  sales>0 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['sales_customer'] = self.cursor.rowcount
        
        dict['sales_withoutSubsequentService'] = dict['bns']
        
        sql = "select * from funnel_customer where  sales>1 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['sales_withrepeatpurchase'] = self.cursor.rowcount
        dict['sales_customerswithaSalesANDServiceRecode'] = dict['bs']
        sql = "select * from funnel_customer where  sales>=1 and `email` is not null and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['sales_totalwithanemail'] = self.cursor.rowcount
        sql = "select * from funnel_customer where  sales>=1 and DATEDIFF(NOW(),last_sales_date)>=730 and DATEDIFF(NOW(),last_service_date)<=1095 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['sales_customerwhopurchased23yearsago'] = self.cursor.rowcount
        sql = "select * from funnel_customer where  sales>=1 and DATEDIFF(NOW(),last_sales_date)>=730 and DATEDIFF(NOW(),last_service_date)<=1095 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['sales_customerwhopurchased23yearsago'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where  sales>=1 and DATEDIFF(NOW(),last_sales_date)>=1095 and DATEDIFF(NOW(),last_service_date)<=1460 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['sales_customerwhopurchased34yearsago'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where  sales>=1 and DATEDIFF(NOW(),last_sales_date)>1460 and DATEDIFF(NOW(),last_service_date)<=1460 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['sales_customerwhopurchased4yearsplus'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where  sales>=1 and DATEDIFF(NOW(),last_sales_date)>0  and DATEDIFF(NOW(),last_service_date)<=30 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['sales_customersSoldaVehicleintheLast30Days'] = self.cursor.rowcount
        
        sql = "select * from funnel_customer where  sales = 1 and DATEDIFF(NOW(),last_sales_date)>0  and DATEDIFF(NOW(),last_service_date)<=30 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['sales_newCustomersSoldaVehicleintheLast30Days'] = self.cursor.rowcount
        
        
        sql = "select * from funnel_customer where  service=1 and DATEDIFF(NOW(),last_service_date)>=0 and DATEDIFF(NOW(),last_service_date)<=30 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['service_newServiceCustomersinLast30Days'] = self.cursor.rowcount
        sql = "select * from funnel_customer where  service>=1 and DATEDIFF(NOW(),last_service_date)>=0 and DATEDIFF(NOW(),last_service_date)<=30 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['service_customersServicedinLast30Days'] = self.cursor.rowcount
        sql = "select * from funnel_customer where  service>=1 and DATEDIFF(NOW(),last_service_date)>720 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['service_pastDueLostCustomer24MonthsorMore'] = self.cursor.rowcount
        sql = "select * from funnel_customer where  service>=1 and DATEDIFF(NOW(),last_service_date)>=540 and DATEDIFF(NOW(),last_service_date)<=720 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['service_pastDueLostCustomer1824Months'] = self.cursor.rowcount
        sql = "select * from funnel_customer where  service>=1 and DATEDIFF(NOW(),last_service_date)>=360 and DATEDIFF(NOW(),last_service_date)<=540 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['service_pastDueLostCustomer1218Months'] = self.cursor.rowcount
        sql = "select * from funnel_customer where  service>=1 and DATEDIFF(NOW(),last_service_date)>=270 and DATEDIFF(NOW(),last_service_date)<=360 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['service_pastDueLostCustomer912Months'] = self.cursor.rowcount
        sql = "select * from funnel_customer where  service>=1 and DATEDIFF(NOW(),last_service_date)>=120 and DATEDIFF(NOW(),last_service_date)<=180 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['service_pastDue46Months'] = self.cursor.rowcount
        sql = "select * from funnel_customer where  service>=1 and DATEDIFF(NOW(),last_service_date)>=90 and DATEDIFF(NOW(),last_service_date)<=120 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['service_due34Months'] = self.cursor.rowcount
        sql = "SELECT * FROM `funnel_customer` WHERE `email` is not null and service>=1 and  fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        dict['service_totalwithanemail'] = self.cursor.rowcount
        self.data = dict
        
    def insert(self,table,dict,cursor,db):
        keylist            = []
        valuelist          = []
        for key,value in dict.iteritems():
            if value       != '':
                keylist.append(key)
                p          = "'" + str(value) + "'"
                valuelist.append(p)
        sql                = "INSERT INTO " + table + '('+','.join(keylist)+')'+'VALUES ('+','.join(valuelist)+')'
        
        cursor.execute(sql)
        db.commit()
        
        return               cursor.lastrowid         
    
    def update(self,table,dict,id,idfield,cursor,db):
        list               = []
        for key,value in dict.iteritems():
            if value      != '':
                p          = key + '=' + "'" + str(value) + "'"
                list.append(p)
        sql                = "UPDATE " + table +" SET " + ','.join(list) + ' where '+ idfield + '=' + "'" + str(id) + "'"
        
        cursor.execute(sql)
        db.commit()                    
    def diff_dates(self,date1, date2):
        return abs(date2-date1).days
    def getAvg(self,n):
        customerid   = n[0]
        sql          = "select * from funnel_customer_roi where type = 1 and fcustomer_id = '%s'" % customerid
        self.cursor.execute(sql)
        sales        = self.cursor.fetchall()
        ent          = 0
        day          = 0
        for s in sales:
            entrydate = s[2]
            year      = s[11]
            make      = s[12]
            model     = s[13]
            if year and make and model:
                sql       = "select * from funnel_customer_roi where type = 2 and year='%s' and make = '%s' and model='%s' and entrydate>='%s' and fcustomer_id = '%s' order by entrydate ASC limit 1" % (year,make,model,entrydate,customerid)
                self.cursor.execute(sql)
                if self.cursor.rowcount == 1:
                   service        = self.cursor.fetchone()
                   ent        = ent  + 1
                   se_entrydate = service[2]
                   day        = day + self.diff_dates(se_entrydate,entrydate)
        return [ent,day]        
                
    
    def sales_averageDaysfromSalesto1stService(self):
        sql = "select * from funnel_customer where  sales>0 and service>0 and fdealer_id='%s'" % self.dealer_id
        self.cursor.execute(sql)
        row      = self.cursor.fetchall()
        ent      = 0
        day      = 0
        for n in row:
            obj  = self.getAvg(n)
            ent  = ent + obj[0]
            day  = ent + obj[1]
        dic  = {}
        dic['sales_averageDaysfromSalesto1stService'] = 0
        if ent > 0:
            if day > 0:
                dic['sales_averageDaysfromSalesto1stService'] = int(day/ent)    
        self.update('funnel_customer_analysis',dic,self.dealer_id,'fdealer_id',self.cursor,self.db)     
        
    def run(self):
        self.process()
        sql = "select * from funnel_customer_analysis where fdealer_id = '%s'" % self.dealer_id
        self.cursor.execute(sql)
        if self.cursor.rowcount == 0:
           self.data['fdealer_id'] = self.dealer_id
           self.insert('funnel_customer_analysis',self.data, self.cursor, self.db) 
        else:
           self.update('funnel_customer_analysis',self.data,self.dealer_id,'fdealer_id',self.cursor,self.db) 
        self.sales_averageDaysfromSalesto1stService()
        self.cursor.close()
        self.db.close()        

            
            