import MySQLdb
from common import *
from geocode import *
import datetime
class roiarchive:
    def __init__(self,dealerid):
        self.db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer_funnel')
        self.cursor = self.db.cursor()
        self.dealerid = dealerid
        self.today    = datetime.date.today()
    def close_database(self):
        self.cursor.close()
        self.db.close()
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
    def run(self):
        t = 100
    def processdata(self):
        dict = {}
        sql  = "select * from funnel_lead where dealerid = '%s'" % self.dealerid
        self.cursor.execute(sql) 
        dict['total_customer'] = self.cursor.rowcount
        sql = "select * from funnel_lead where isdob = 1 and dealerid='%s'" % self.dealerid
        self.cursor.execute(sql)
        dict['birthday'] = self.cursor.rowcount
        sql = "select * from funnel_lead where warrantydate <= '%s' and dealerid='%s'" % (self.today,self.dealerid)
        self.cursor.execute(sql)
        dict['warrantyexpiration'] = self.cursor.rowcount
        sql = "select * from funnel_lead where leasedate <= '%s' and dealerid='%s'" % (self.today,self.dealerid)
        self.cursor.execute(sql)
        dict['leaseexpiration'] = self.cursor.rowcount
        
                