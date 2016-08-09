from datetime import date, timedelta as td
import datetime
import MySQLdb
class customerarchive:
    def __init__(self):
        self.startdate = date(2015, 1, 1)
        self.enddate   = date(2015, 1, 10)
        self.calculatedaterange()
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
    def updatecrontable(self):
        now = datetime.datetime.now()
        sql = "update funnel_cron_flag set status = '1',date='%s',errorlog='""',iserror='0' where id = 2" % now
        self.cursor.execute(sql)
        self.db.commit()  
    def startprocess(self):
        return True
        '''
        self.connect_database(2)
        sql = "select * from funnel_cron_flag where id = 2 and status = 0"
        self.cursor.execute(sql)
        if self.cursor.rowcount == 1:
            self.updatecrontable()
            self.close_database()
            return True
        else:
            self.close_database()
            return False
        '''    
    def getdealer(self):
        self.fdealer_id = 4
        self.dealerid = '300886' 
        '''
        sql    = "update funnel_dealer set flag = 1 where id='%s'" % self.fdealer_id
        self.cursor.execute(sql)
        self.db.commit()
        self.close_database()
        '''
    def endprocess(self):
        sql = "update funnel_cron_flag set status = '0' where id = 2"
        self.cursor.execute(sql)
        self.db.commit()
    def calculatedaterange(self):
        delta = self.enddate - self.startdate
        lst   = []
        for i in range(delta.days + 1):
            lst.append(self.startdate + td(days=i))        
        self.daterange = lst 
    def getSalesCustomer(self,date):
        self.connect_database()
        sql = "SELECT distinct `cid` FROM `sale` WHERE `dealer_id`='%s' and deal_date<='%s'" % (self.dealerid,date)
        self.cursor.execute(sql)
        sales_customer = []
        sales = self.cursor.fetchall()
        for n in sales:
            sales_customer.append(n[0])
        return  sales_customer
    def getServiceCustomer(self,date):
        self.connect_database()
        sql = "SELECT distinct `cid` FROM `service` WHERE `dealer_id`='%s' and close_date<='%s'" % (self.dealerid,date)
        self.cursor.execute(sql)
        sales_customer = []
        sales = self.cursor.fetchall()
        for n in sales:
            sales_customer.append(n[0])
        return  sales_customer
    def diff_dates(self,date1, date2):
        return abs(date2-date1).days
    def getStatus(self,date):
        active = 0
        lessactive = 0
        lost  = 0
        for n in self.customer:
            lastactivity = ''
            sql = "select * from sale where cid = '%s' and dealer_id = '%s' and deal_date<='%s' order by deal_date DESC limit 1" % (n,self.dealerid,date)
            self.cursor.execute(sql)
            salescount = self.cursor.rowcount
            if salescount > 0:
                salesrow = self.cursor.fetchone()
                salesdate = salesrow[8]
            sql = "select * from service where cid = '%s' and dealer_id = '%s' and close_date<='%s' order by close_date DESC limit 1 " % (n,self.dealerid,date)
            self.cursor.execute(sql)
            service    = self.cursor.rowcount
            if service > 0:
                servicerow = self.cursor.fetchone()
                servicedate = salesrow[8]
            if  salescount > 0 and service > 0:
                if  salesdate > servicedate:
                    lastactivity = salesdate
                else:
                    lastactivity = servicedate
            elif  salescount > 0 and service == 0:
                lastactivity = salesdate
            else:
                lastactivity = servicedate
            diff = self.diff_dates(date, lastactivity) 
            if diff >=  180: 
               active = active + 1
            elif diff < 180 and diff>=365:
               lessactive = lessactive + 1
            else:
               lost = lost + 1
        return [active,lessactive,lost]                                      
            
    def getBNS(self,date):
        salesonly = 0
        serviceonly = 0
        both  = 0
        for n in self.customer:
            sql = "select * from sale where cid = '%s' and dealer_id = '%s' and deal_date<='%s'" % (n,self.dealerid,date)
            self.cursor.execute(sql)
            salescount = self.cursor.rowcount
            sql = "select * from service where cid = '%s' and dealer_id = '%s' and close_date<='%s'" % (n,self.dealerid,date)
            self.cursor.execute(sql)
            servicecount = self.cursor.rowcount
            if salescount > 0 and servicecount == 0:
               salesonly = salesonly + 1
            elif salescount == 0 and servicecount > 0:
               serviceonly = serviceonly + 1
            elif salescount > 0 and servicecount > 0:
               both = both + 1          
        return [salesonly,serviceonly,both]        
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
    def process(self):
        if self.startprocess():
            self.getdealer()
            self.connect_database()
            lst = []
            for n in self.daterange:
                dic   = {}
                sales_customer = self.getSalesCustomer(n)
                service_customer = self.getServiceCustomer(n) 
                customer= list(set(sales_customer)|set(service_customer)) 
                self.total = len(customer)
                self.customer = customer
                s_analysis = self.getBNS(n)
                status_analysis = self.getStatus(n)
                dic['date'] = n
                dic['total'] = self.total
                dic['active'] = s_analysis[0]
                dic['lessactive'] = s_analysis[1]
                dic['lost'] = s_analysis[2]
                dic['salesonly'] = status_analysis[0]
                dic['serviceonly'] = status_analysis[1]
                dic['bothroi'] = status_analysis[2]
                dic['fdealer_id'] = self.fdealer_id
                self.close_database()
                self.connect_database(2)
                print dic
                #self.insert('funnel_customer_archive',dic,self.cursor,self.db)
                self.close_database()
                self.connect_database()
            self.close_database()
            self.connect_database(2)
            self.endprocess()
            self.close_database()
            
        
p = customerarchive()
p.process()   