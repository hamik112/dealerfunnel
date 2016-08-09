import MySQLdb
import math
from datetime import datetime
class customer_status:
    def __init__(self):
        self.db            = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
        #self.db            = MySQLdb.connect('localhost','root','123456','dealerfunnel')
        self.cursor        = self.db.cursor()
    def getindex(self,tablename,column):
        sql = "SHOW COLUMNS from %s" % tablename
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        i=0;
        for row in results:
            if row[0] == column:
                return i
            else:
                i = i + 1
        return 0
    def insert(self,table,dict):
        keylist            = []
        valuelist          = []
        for key,value in dict.iteritems():
            if value       != '':
                keylist.append(key)
                p          = "'" + str(value) + "'"
                valuelist.append(p)
        sql                = "INSERT INTO " + table + '('+','.join(keylist)+')'+'VALUES ('+','.join(valuelist)+')'
        
        self.cursor.execute(sql)
        self.db.commit()
        return               self.cursor.lastrowid         
    
    def update(self,table,dict,id,idfield):
        list               = []
        for key,value in dict.iteritems():
            if value      != '':
                p          = key + '=' + "'" + str(value) + "'"
                list.append(p)
        sql                = "UPDATE " + table +" SET " + ','.join(list) + ' where '+ idfield + '=' + "'" + str(id) + "'"
        
        print sql
        self.cursor.execute(sql)
        self.db.commit()
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
    def customer_refress(self):
        sql = "select * from funnel_customer where flag1='0' limit 1"
        self.cursor.execute(sql)
        if self.cursor.rowcount == 0:
            sql = "UPDATE funnel_customer set flag1='0'"
            self.cursor.execute(sql)
            self.db.commit()
    def customer_update(self):
        sql = "select * from funnel_customer where flag1='0' limit 100"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for row in results:
            id     = row[0]
            date   = row[self.getindex('funnel_customer','lastvisit')]       
            status = self.calculate_status(date)
            dict   = {"status":status,"flag1":1}
            self.update('funnel_customer',dict,id,'id')
            
customer_status().customer_refress()
customer_status().customer_update()             
          
    
    
        
                    