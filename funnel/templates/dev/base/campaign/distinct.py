import MySQLdb
import hashlib
from common import *
from loadlead import *
from customer_analysis import *
import datetime

class dist:
     def __init__(self):
        self.db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer_funnel')
        self.cursor = self.db.cursor()
     def collectdist(self):
         sql = "select distinct `fservice` from funnel_customer_roi where 1"   
         self.cursor.execute(sql)
         data = self.cursor.fetchall()
         lst = []
         for n in data:
             lst.append(n[0])
         self.distid = lst
     def getindex(self,tablename,column,cursor):
        sql = "SHOW COLUMNS from %s" % tablename
        cursor.execute(sql)
        results = cursor.fetchall()
        i=0;
        for row in results:
            if row[0] == column:
                return i
            else:
                i = i + 1
        return 0
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
     def customerrepairproffit(self):
         #SELECT sum(`invoiced`) FROM `funnel_customer_roi` WHERE type = 2 and `fcustomer_id`=100003348
         sql = "SELECT * FROM `funnel_customer` WHERE `service`>0" 
         self.cursor.execute(sql)
         data = self.cursor.fetchall()
         for n in data:
             dcs = {}
             sale  = n[18]
             bar   = n[0]
             sql1  = "SELECT sum(`invoiced`) FROM `funnel_customer_roi` WHERE type = 2 and `fcustomer_id`= '%s'" % bar
             self.cursor.execute(sql1)
             result = self.cursor.fetchone()
             dcs['invoiced'] = result[0]
             self.update('funnel_customer',dcs,bar,'id', self.cursor, self.db)
             print bar
     def customerrepair(self):
         #SELECT sum(`invoiced`) FROM `funnel_customer_roi` WHERE type = 2 and `fcustomer_id`=100003348
         sql = "SELECT * FROM `funnel_customer` WHERE `service`>0" 
         self.cursor.execute(sql)
         data = self.cursor.fetchall()
         for n in data:
             dcs = {}
             sale  = n[18]
             bar   = n[0]
             sql1  = "select * from funnel_customer_roi where type= 2 and  fcustomer_id = '%s'" % bar
             self.cursor.execute(sql1)
             count = self.cursor.rowcount
             dcs['service'] = count
             dcs['visit'] = count + sale
             self.update('funnel_customer',dcs,bar,'id', self.cursor, self.db)
             print bar
             
     def repair(self):
         self.collectdist()
         lst = []
         distid = self.distid
         lst.append(self.distid[2])
         for n in distid:
             if n:
                 sql = "select * from funnel_customer_roi where fservice = '%s' limit 1" % n
                 self.cursor.execute(sql)
                 result = self.cursor.fetchone()
                 
                 dic  = {}
                 dic['type'] = 2
                 dic['entrydate'] = result[2]
                 dic['warrantyexpiration'] = result[3]
                 dic['leaseexpiration'] = result[4]
                 dic['grossprofit'] = result[5]
                 dic['invoiced'] = result[6]
                 dic['year'] = result[7]
                 dic['make'] = result[8]
                 dic['model'] = result[9]
                 dic['tyear'] = result[10]
                 dic['tmake'] = result[11]
                 dic['tmodel'] = result[12]
                 dic['tradedate'] = result[13]
                 dic['istradein'] = result[14]
                 dic['fsales'] = result[15]
                 dic['fservice'] = result[16]
                 dic['fcustomer_id'] = result[17]
                 dic['fdealer_id'] = result[18]
                 sql1 = "delete from funnel_customer_roi where fservice = '%s'" % n
                 self.cursor.execute(sql1)
                 self.db.commit()
                 print n
                 print self.insert('funnel_customer_roi', dic, self.cursor, self.db)
                 
dist().customerrepairproffit()         
             
