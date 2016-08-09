from datetime import date, timedelta as td
import datetime
import MySQLdb
class customerarchive:
    def __init__(self):
        self.startdate = date(2008, 1, 1)
        self.enddate   = date(2016, 4, 15)
        self.connect_database()
        self.calculatedaterange()
    def connect_database(self,flag = 1):
        self.db     = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
        self.cursor = self.db.cursor()    
    def close_database(self):
        self.cursor.close()
        self.db.close()    
    def getdealer(self):
        self.fdealer_id = 9
        self.dealerid = 9
    
    def calculatedaterange(self):
        delta = self.enddate - self.startdate
        lst   = []
        for i in range(delta.days + 1):
            lst.append(self.startdate + td(days=i))        
        self.daterange = lst 
    def getSalesCustomer(self):
        self.connect_database()
        sql = "SELECT distinct `fcustomer_id` FROM `funnel_customer_roi` WHERE `fdealer_id`='%s' and type = 1" % self.dealerid
        self.cursor.execute(sql)
        sales_customer = []
        sales = self.cursor.fetchall()
        for n in sales:
            sales_customer.append(n[0])
        self.close_database()    
        return  sales_customer
    def getServiceCustomer(self):
        self.connect_database()
        sql = "SELECT distinct `fcustomer_id` FROM `funnel_customer_roi` WHERE `fdealer_id`='%s' and type = 2" % self.dealerid
        self.cursor.execute(sql)
        sales_customer = []
        sales = self.cursor.fetchall()
        for n in sales:
            sales_customer.append(n[0])
        self.close_database()    
        return  sales_customer
    def diff_dates(self,date1, date2):
        return abs(date2-date1).days
    
    
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
    def getCustomerId(self):
        sales_customer = self.getSalesCustomer()
        service_customer = self.getServiceCustomer() 
        self.customeridList= list(set(sales_customer)|set(service_customer))
        
    def mapCustomer(self):
        self.connect_database()
        dic   = {}
        for n in self.customeridList:
            sql    = "select * from funnel_customer_roi where fcustomer_id = '%s' and fdealer_id='%s' and type = 1 order by  entrydate DESC" % (n,self.dealerid)
            self.cursor.execute(sql)
            saleslst   = []
            if self.cursor.rowcount > 0:  
                sales = self.cursor.fetchall()
                for s in sales:
                    saleslst.append(s[2])
            
            sql    = "select * from funnel_customer_roi where fcustomer_id = '%s' and fdealer_id='%s' and type = 2 order by  entrydate DESC" % (n,self.dealerid)
            self.cursor.execute(sql)
            servicelst   = []
            if self.cursor.rowcount > 0:  
                service = self.cursor.fetchall()
                for s in service:
                    servicelst.append(s[2]) 
            dic[n] = {"sale":saleslst,"service":servicelst}    
        self.mapId = dic
        self.close_database()            
    def getIscustomer(self,dt,daterange):
        temp       =  date(1999, 4, 3)
        flag       = 0
        for n in daterange:
            if n:
                if dt >= n:
                    flag = 1
                    if temp < n:
                        temp = n
        
        return {"is":flag,'lastvisit':temp}              
    def getCustomerStatusForAData(self,dt,sale,service):
        dic  = {"iscustomer":0,"active":0,'lessactive':0,'lost':0,'salesonly':0,'serviceonly':0,'both':0}
        status = self.getIscustomer(dt,sale+service)
        if status['is'] == 1:
            dic['iscustomer'] = 1
            lastvisit = status['lastvisit']
            if lastvisit<=dt:
                date_diff = self.diff_dates(dt,lastvisit)
                if date_diff <=180:
                    
                    dic['active'] = 1
                elif date_diff > 180 and date_diff <= 365:
                    dic['lessactive'] = 1
                else:
                    dic['lost'] = 1        
            isSale = 0
            for n in sale:
                if dt >= n:
                   isSale = 1
            isService = 0
            for n in service:
                if dt >= n:
                   isService = 1
            if isSale == 1 and  isService == 1:
               dic['both'] = 1
            elif isSale == 1 and isService == 0:
               dic['salesonly'] = 1
            elif isSale == 0 and isService == 1:
               dic['serviceonly'] = 1                 
        return dic                
    
    def process(self):
        self.getdealer()
        self.getCustomerId()
        self.mapCustomer()
        self.cid  = []
        for dt in self.daterange:
            dic  = {"fdealer_id":self.fdealer_id,"date":dt,"total":0,"active":0,'lessactive':0,'lost':0,'salesonly':0,'serviceonly':0,'bothroi':0}
            for key, value in self.mapId.iteritems():
                res = self.getCustomerStatusForAData(dt,value['sale'],value['service'])    
                dic['total'] = res['iscustomer'] + dic['total']
                dic['active'] = res['active'] + dic['active']
                dic['lessactive'] = res['lessactive'] + dic['lessactive']
                dic['lost'] = res['lost'] + dic['lost']
                dic['salesonly'] = res['salesonly'] + dic['salesonly']
                dic['serviceonly'] = res['serviceonly'] + dic['serviceonly']
                dic['bothroi'] = res['both'] + dic['bothroi']
            print dic
            self.connect_database(2)
            self.insert('funnel_customer_archive',dic,self.cursor,self.db)
            self.close_database()
            
p = customerarchive()
p.process()

   