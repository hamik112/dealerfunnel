import MySQLdb
import hashlib
from common import *
from loadlead import *
from customer_analysis import *
import datetime
import sys, os
class process:
    def connect_database(self,flag = 1):
        if flag == 1:
            self.db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer')
            self.cursor = self.db.cursor()
        else:
            self.db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer_funnel')
            self.cursor = self.db.cursor()
    def close_database(self):
        self.cursor.close()
        self.db.close()
    def startprocess(self):
        sql = "select * from funnel_cron_flag where id = 1 and status = 0"
        self.cursor.execute(sql)
        if self.cursor.rowcount == 1:
            self.updatecrontable()
            return True
        else:
            return False
        
        
    def endprocess(self):
        sql = "update funnel_cron_flag set status = '0' where id = 1"
        self.cursor.execute(sql)
        self.db.commit()
    def checkdealerstatus(self):
        sql  = "select * from funnel_dealer where status = 1 and processed_flag = 0"
        self.cursor.execute(sql)                    
        if self.cursor.rowcount == 0:
            sql = "update funnel_dealer set processed_flag = 0"
            self.cursor.execute(sql)
            self.db.commit()
    def updatecrontable(self):
        now = datetime.datetime.now()
        sql = "update funnel_cron_flag set status = '1',date='%s',errorlog='""',iserror='0' where id = 1" % now
        self.cursor.execute(sql)
        self.db.commit()    
    def getdealer(self):
        sql  = "select * from funnel_dealer where status = 1 and processed_flag = 0 limit 1"
        self.cursor.execute(sql)         
        dealer = self.cursor.fetchone()
        self.dealerid = dealer[0] 
        self.dealerzipid = dealer[5]
        self.dealer_consumerid = dealer[48]
        count  = dealer[50] + 1
        self.croncount = count
        sql    = "update funnel_dealer set processed_flag = 1 where id='%s'" % self.dealerid
        self.cursor.execute(sql)
        self.db.commit() 
        return  dealer
    def getSales(self):
        sql  = "select * from sale where processed_flag = 0 and dealer_id = '%s' order by deal_date DESC" % self.dealer_consumerid
        self.cursor.execute(sql) 
        self.salescount = self.cursor.rowcount
        self.sales      = self.cursor.fetchall()
    def getService(self):
        sql  = "select * from service where processed_flag = 0 and dealer_id = '%s' order by close_date DESC" % self.dealer_consumerid
        self.cursor.execute(sql) 
        self.servicecount = self.cursor.rowcount
        self.service      = self.cursor.fetchall()
    def getZipcode(self):
        sql  = "select * from funnel_zipcode where id='%s'" % self.dealerzipid
        self.cursor.execute(sql)    
        result = self.cursor.fetchone()
        self.dealerzipcode = result[1] 
    def updatedealer(self):
        sql = "update funnel_dealer set processed_flag = 1 where id='%s'" % self.dealerid
        self.cursor.execute(sql)
        self.db.commit()
    def isRoi(self,type,n):
        return True
        id      = n[0]
        self.connect_database(2)
        if type == 1:
            sql = "select * from funnel_customer_roi where fsales = '%s' limit 1" % id
        else:
            sql = "select * from funnel_customer_roi where fservice = '%s' limit 1" % id     
        self.cursor.execute(sql)
        if self.cursor.rowcount == 1:
            self.close_database()
            return False
        else:
            self.close_database()
            return True
    def updatecronbeforeprocess(self,type,n):
        id      = n[0]
        self.connect_database(2)
        sql = "update funnel_cron_flag set typeid = '%s',type='%s',dealerid='%s',iserror=0 where id = 1" % (id,type,self.dealerid) 
        self.cursor.execute(sql)
        self.db.commit()    
        self.close_database()
    def exceptionhandle(self,e):
        self.connect_database(2)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        lst   = str(exc_type) + ' ' + str(fname) + ' ' +  str(exc_tb.tb_lineno) + ' ' +  str(e.__doc__) + ' ' + str(e.message)
        lst   = lst.replace("'","\\'")
        sql = "update funnel_cron_flag set errorlog='%s',iserror=1 where id = 1" % lst 
        self.cursor.execute(sql)
        self.db.commit()    
        self.close_database()            
    def updateroiprocess(self,data,type = 1):
        self.connect_database()
        if type == 1:
            slid = data[0]
            sql  = "update sale set processed_flag = 1 where slid = '%s'" % slid
        else:
            svid = data[0]
            sql  = "update service set processed_flag = 1 where svid = '%s'" % svid            
        self.cursor.execute(sql)
        self.db.commit()
        self.close_database()     
    def run(self):
        self.connect_database(2)
        if self.startprocess():
           self.checkdealerstatus()
           dealer = self.getdealer()
           self.getZipcode()
           self.marketout   = dealer[44]
           self.close_database()
           self.connect_database()
           self.getSales()
           self.getService()
           self.close_database()
           if self.salescount > 0:
              i = 0
              for n in self.sales:
                  if self.isRoi(1,n):
                      #self.updatecronbeforeprocess(1,n)
                      
                      try:
                          processlead(self.dealerid,self.dealerzipcode,self.marketout,self.dealer_consumerid).processbysaleservice(n,1)
                      except Exception as e:
                          self.exceptionhandle(e)
                          return ''
                      self.updateroiprocess(n,1)
                       
                        
           if self.servicecount > 0:
              i = 0
              for n in self.service:
                  if self.isRoi(2,n):
                      #self.updatecronbeforeprocess(2,n)
                      try:
                          processlead(self.dealerid,self.dealerzipcode,self.marketout,self.dealer_consumerid).processbysaleservice(n,2)
                      except Exception as e:
                          self.exceptionhandle(e)
                          return ''         
                      self.updateroiprocess(n,2)
           #customer_analysis(self.dealerid).run()
           self.connect_database(2)
           self.endprocess()
           self.updatedealer()
           self.close_database()
        else:
           self.close_database()     
    def runprocess(self):
        self.run()                
process().runprocess()                      
        