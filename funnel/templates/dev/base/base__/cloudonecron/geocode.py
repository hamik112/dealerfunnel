import urllib2
import urllib
import json
import unirest
import MySQLdb
class geocode:
    def __init__(self,zip1,zip2=''):
        self.zip1   = zip1
        self.zip2   = zip2
        self.key   = 'AIzaSyAPJzJJ2W3NhCo7jwaQJqvPdZdJoem27Ss'
    def isset(self,variable):
        return variable in locals() or variable in globals()
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
    def getlatlng(self):
        response = unirest.get("https://redline-redline-zipcode.p.mashape.com/rest/info.json/"+ str(self.zip1) +"/degrees",
        headers={
                "X-Mashape-Key": "VxqTwZsHqomshtOynyJnIUGYbyolp1eZz09jsnIqzhNjaepf1Y",
                "Accept": "application/json"
                })
        latlng = [0,0]                       
        if 'error_code' in response.body:
            return latlng
        else:
            if 'lat' in response.body:
                latlng[0] = response.body['lat']
                latlng[1] = response.body['lng']
                return latlng
            else:
                return latlng
    
    def distance(self):
         response = unirest.get("https://redline-redline-zipcode.p.mashape.com/rest/distance.json/" + str(self.zip1) + "/" + str(self.zip2) + "/km",
         headers={
                   "X-Mashape-Key": "VxqTwZsHqomshtOynyJnIUGYbyolp1eZz09jsnIqzhNjaepf1Y",
                   "Accept": "application/json"
                 })
         if 'error_code' in response.body:
            return -1
         else:
            if 'distance' in response.body:
                return response.body['distance']
            else:
                return -1   
    def distanceWrapper(self):
        db     = MySQLdb.connect('161.47.5.163','xcel','GZaSTXUY3ZK2XKPE','consumer_funnel')
        cursor = db.cursor()
        flag   = 0
        sql    = "select * from funnel_zipcode_distance where zip1 = '%s' and zip2 = '%s' " % (self.zip1,self.zip2)
        cursor.execute(sql)
        if cursor.rowcount == 1:
            result = cursor.fetchone()
            return result[3]
        sql    = "select * from funnel_zipcode_distance where zip1 = '%s' and zip2 = '%s' " % (self.zip2,self.zip1)
        cursor.execute(sql)
        if cursor.rowcount == 1:
            result = cursor.fetchone()
            return result[3]      
        val  = self.distance()
        dict = {"zip1":self.zip1,"zip2":self.zip2,"val":val}
        self.insert('funnel_zipcode_distance',dict,cursor,db)
        dict = {"zip1":self.zip2,"zip2":self.zip1,"val":val}
        self.insert('funnel_zipcode_distance',dict,cursor,db)
        cursor.close()
        db.close()
        return val            