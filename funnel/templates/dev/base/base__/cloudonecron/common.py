import MySQLdb
import math
from geocode import geocode
from datetime import datetime
import hashlib
import time
class common:
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