import MySQLdb
import hashlib
from mapzipcode import *

class dealerimport:
    def __init__(self):
        self.dealer = {}
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
    def getDealerFromConsumer(self):
        self.connect_database()
        sql =  "select * from dealers"
        self.cursor.execute(sql)
        self.dealer = self.cursor.fetchall() 
        self.close_database()
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
    def convertstr(self,var):
        return var.replace("'","\\'")
    def stringtohash(self,val):
        return hashlib.sha224(val).hexdigest()
    def insertDealer(self):
        self.connect_database(2)
        for n in self.dealer:
            sql = "select * from funnel_dealer where dealerid = %s" % n[0]
            self.cursor.execute(sql)
            if self.cursor.rowcount == 0:
                   dict = {}
                   dict['dealerid']  = n[0]
                   dict['name']      = self.convertstr(n[1])
                   dict['address']   = n[2]
                   dict['city']      = n[3]
                   dict['state']     = n[4]
                   dict['fzip_id']   = mapzip(n[5],self.db,self.cursor).setZip()
                   dict['flogo_id']  = 1
                   dict['fmlogo_id'] = 1
                   dict['keyid']     = self.stringtohash(str(n[0])) 
                   self.insert('funnel_dealer',dict, self.cursor, self.db)

cron = dealerimport()
cron.getDealerFromConsumer()
cron.insertDealer()
                                  