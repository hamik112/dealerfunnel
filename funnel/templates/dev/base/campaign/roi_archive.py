import MySQLdb
from common import *
from geocode import *
class roiarchive:
    def __init__(self,roi,dealerid,type = 1):
        self.db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer_funnel')
        self.cursor = self.db.cursor()
        self.roi    = roi
        self.type   = type
        self.dealerid = dealerid
        self.processdata()
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
        sql = "select * from funnel_roi_archive where date = '%s' and dealerid = '%s' limit 1" % (self.date,self.dealerid)
        self.cursor.execute(sql) 
        dict = {}
        if self.cursor.rowcount == 1:
            data = self.cursor.fetchone()
            id   = data[0]
            if self.type == 1:
                dict['sales']       = data[2] + 1
                dict['grossprofit'] = float(data[4]) + float(self.grossprofit)
            else:
                dict['service']     = data[3] + 1
                dict['roammount']   = float(data[5]) + float(self.roammount)
            
            self.update('funnel_roi_archive',dict,id,'id', self.cursor, self.db)    
        else:
            if self.type == 1:
                dict['sales']       = 1
                dict['grossprofit'] = self.grossprofit
                dict['service']     = 0
                dict['roammount']   = 0
            else:
                dict['sales']       = 0
                dict['grossprofit'] = 0
                dict['service']     = 1
                dict['roammount']   = self.roammount
            dict['date']        = self.date
            dict['dealerid']    = self.dealerid
            self.insert('funnel_roi_archive',dict,self.cursor,self.db)  
        self.close_database()
    def processdata(self):
        self.sale        = 0
        self.grossprofit = 0 
        self.service     = 0
        self.roammount   = 0  
        if self.type == 1:
           self.date  = self.roi[8]
           self.sale  = 1
           self.grossprofit = self.roi[12]   
           self.roammount  = 0  
        else:
           self.date  = self.roi[8]
           self.service  = 1
           self.roammount  = self.roi[10]
           self.grossprofit = 0
                