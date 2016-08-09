import MySQLdb
from common import *
from geocode import *
from roi_archive import *
from mapzipcode import *
from historical_report import *
import datetime
import warnings
warnings.filterwarnings('ignore')
class processlead:
    def __init__(self,dealerid,dealerzip,marketout,dealer_consumerid):
        self.dealerzip = dealerzip
        self.marketout = marketout
        self.dealerid  = dealerid
        self.dealer_consumerid = dealer_consumerid
        
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
    def isConsumer(self,id):
        sql = "select * from funnel_customer where consumerid = %s and fdealer_id = '%s' limit 1" % (id,self.dealerid)
        self.connect_database(2)
        self.cursor.execute(sql)
        flag = self.cursor.rowcount
        self.close_database()
        if flag == 1:
            return True
        else:
            return False
    def convertstr(self,var):
        return var.replace("'","\\'")
    def getmail(self,id):
        self.connect_database()
        sql = "SELECT DISTINCT email FROM consumer.source_id id, consumer.email em WHERE id.eid_1 = em.eid AND id.dealer_id = %s AND id.cid = %s ORDER BY date_transaction DESC" % (self.dealer_consumerid,id)
        self.cursor.execute(sql)
        dict3 = {}
        if self.cursor.rowcount == 1:
            dict3['isemail'] = 1
            email = self.cursor.fetchone()
            dict3['email'] = email[0]
        else:
            dict3['isemail'] = 0
            dict3['email'] = ''
        return dict3    
    def getname(self,consumer):
        self.connect_database()
        dict1          = {}
        dict1['fname'] = self.convertstr(consumer[common().getindex('consumer','name_first',self.cursor)])
        dict1['lname'] = self.convertstr(consumer[common().getindex('consumer','name_middle',self.cursor)]) + ' ' + self.convertstr(consumer[common().getindex('consumer','name_last',self.cursor)])
        dict1['birth_date'] = consumer[common().getindex('consumer','dob',self.cursor)]
        if dict1['fname'] is None:
            dict1['fname'] = 'Unknown'
        if dict1['birth_date'] is None:
            dict1['isbirthday'] = 0
        else:
            dict1['isbirthday'] = 1        
        self.close_database()
        return dict1
    def getAddress(self,id):
        self.connect_database()
        sql = "select * from address where cid = '%s' limit 1" % id
        self.cursor.execute(sql)
        dict2 = {}
        dict2['ismarketout'] = 0
        if self.cursor.rowcount == 1:
           consumeraddress = self.cursor.fetchone()
           dict2['address'] = self.convertstr(consumeraddress[common().getindex('address','address1',self.cursor)])
           dict2['city']  = self.convertstr(consumeraddress[common().getindex('address','city',self.cursor)])
           dict2['state'] = self.convertstr(consumeraddress[common().getindex('address','state',self.cursor)])
           zip            = consumeraddress[common().getindex('address','zip',self.cursor)]
           self.close_database()
           self.connect_database(2)
           dict2['fzip_id']  = mapzip(zip,self.db,self.cursor).setZip()
           dict2['distance'] = geocode(zip,self.dealerzip).distanceWrapper()
           self.close_database()
           if dict2['distance'] == -1:
               dict2['ismarketout'] = 1
               
           return dict2
        else:
           dict2 = {"address":"","city":"","state":"","fzip_id":13,"distance":-1,"ismarketout":0}
           self.close_database()
           return dict2
    def getPhone(self,id):
        self.connect_database()
        dict3 = {}
        dict3['homephone']   = ''
        dict3['workphone']   = ''
        dict3['cellphone']   = ''
        sql = "select * from phone where cid = %s" % id
        self.cursor.execute(sql)        
        phone = self.cursor.fetchall()
        for n in phone:
            if n[3] == 'Cell':
                dict3['cellphone'] = n[2]
            if n[3] == 'Work':
                dict3['workphone'] = n[2]
            if n[3] == 'Home':
                dict3['homephone'] = n[2]
        self.close_database()
        return dict3         
    
        #return tmp
                 
        
        
    def hashkey(self,val):
        return hashlib.sha224(val).hexdigest()
    def setTopVehicle(self,vehicle):
        make  = vehicle['tmake']
        model = vehicle['tmodel']
        self.connect_database(2)
        sql   = "select * from funnel_topvehicle where make = '%s' and model = '%s'" % (make,model)
        self.cursor.execute(sql)
        if self.cursor.rowcount == 1:
           vehicle = self.cursor.fetchone()
           id      = vehicle[0]
           count   = vehicle[3] 
           dict    = {"count":count+1}
           common().update('funnel_topvehicle',dict,id,'id', self.cursor, self.db)
        else:
           dict    = {"make":make,"model":model,"count":1,"fdealer_id":self.dealerid}
           common().insert('funnel_topvehicle',dict,self.cursor,self.db)
        self.close_database()       
    
    def getLeadInfo(self,consumerid):
        self.connect_database(2)
        sql = "select * from funnel_customer where consumerid = '%s' and fdealer_id='%s' limit 1" % (consumerid,self.dealerid)
        self.cursor.execute(sql)
        lead = self.cursor.fetchone()
        lst  = ['lastvisit','last_sales_date','last_service_date','id','visit','sales','service','grossprofit','invoiced']
        dict = {}
        for n in lst:
            dict[n] = lead[common().getindex('funnel_customer',n,self.cursor)]  
        return dict
        self.close_database()
        
    
    def diff_dates(self,date1, date2):
        return abs(date2-date1).days
    def getroi(self,roi,type = 1):
        self.connect_database()
        dict = {}
        dict['sales']   = 0
        dict['service'] = 0 
        dict['visit'] = 1
        dict['last_sales_date'] = 0
        dict['last_service_date'] = 0
        dict['grossprofit'] = 0   
        dict['invoiced'] = 0
        dict['lastvisit'] = 0  
        dict['status'] = 1
        if type == 1:
           dict['sales']   = 1
           dict['last_sales_date'] =  roi[common().getindex('sale','deal_date',self.cursor)] 
           dict['lastvisit'] =  roi[common().getindex('sale','deal_date',self.cursor)] 
           dict['grossprofit'] =  roi[common().getindex('sale','gross_profit_sale',self.cursor)]   
        else:
           dict['service']   = 1
           dict['last_service_date'] =  roi[common().getindex('service','close_date',self.cursor)] 
           dict['lastvisit'] =  roi[common().getindex('service','close_date',self.cursor)] 
           dict['invoiced'] =  roi[common().getindex('service','ro_amount',self.cursor)]    
        today    =  datetime.date.today()
        diff     = self.diff_dates(today,dict['lastvisit'])
        if diff <= 180:
           dict['status'] = 1
        elif diff >180 and diff < 365:
           dict['status'] = 2
        else:
           dict['status'] = 3         
        self.close_database()
        return dict
    def checkTrade(self,sales,leadid):
        flag = False 
        self.connect_database()
        slid  = sales[common().getindex('sale','slid',self.cursor)]
        sql   = "select * from sale_trade where slid = '%s' limit 1" % slid  
        self.cursor.execute(sql)
        if self.cursor.rowcount == 1:
            tradedata = self.cursor.fetchone()
            dict      = {}
            dict['tid']  = slid
            dict['date'] = tradedata[common().getindex('sale_trade','daterange',self.cursor)]
            vid          = tradedata[common().getindex('sale_trade','vid',self.cursor)] 
            sql = "select * from vehicle where vid='%s' limit 1" % vid
            self.cursor.execute(sql)
            if self.cursor.rowcount == 1:
                flag = True
                vehicle = self.cursor.fetchone()
                dict['year'] = vehicle[common().getindex('vehicle','year',self.cursor)]
                dict['lead_id'] = leadid
                self.close_database()
                self.connect_database(2)
                common().insert('funnel_lead_trade', dict, self.cursor, self.db)
                dict = {"istrade":1}
                common().update('funnel_lead',dict,leadid,'id', self.cursor, self.db)
        self.close_database()
        if flag:
            #self.setTopVehicle(vehicle)
            t = 0    
    def getTrade(self,sid):
        sql   = "select * from sale_trade where slid = '%s' limit 1" % sid  
        self.cursor.execute(sql)
        dic   = {"istradein":0,"tradedate":None,"tyear":"","tmake":"","tmodel":""}
        if self.cursor.rowcount == 1:
            tradedata = self.cursor.fetchone()
            dic['tradedate']   = tradedata[common().getindex('sale_trade','daterange',self.cursor)]
            dic['istradein']   = 1
            vid                 = tradedata[common().getindex('sale_trade','vid',self.cursor)]
            tmp                 = self.getVehicle(vid)
            dic['tyear']       = tmp['year']
            dic['tmake']       = tmp['make']
            dic['tmodel']      = tmp['model']
            
        return dic    
    def getVehicle(self,vid):
        sql = "select * from vehicle where vid='%s' limit 1" % vid
        self.cursor.execute(sql)
        dic = {"year":'',"make":"","model":""}
        if self.cursor.rowcount == 1:
            vehicle = self.cursor.fetchone()
            dic['year'] = vehicle[common().getindex('vehicle','year',self.cursor)]
            dic['make'] = vehicle[common().getindex('vehicle','make',self.cursor)]
            dic['model'] = vehicle[common().getindex('vehicle','model',self.cursor)]
        return dic
    def insertServiceRoi(self,roi,customerid):
        self.connect_database()
        dic = {}
        dic['type'] = 2
        dic['istradein'] = 0
        dic['entrydate'] = roi[common().getindex('service','close_date',self.cursor)] 
        dic['invoiced'] = roi[common().getindex('service','ro_amount',self.cursor)]
        dic['fservice'] = roi[common().getindex('service','svid',self.cursor)]
        vid             = roi[common().getindex('service','vid',self.cursor)]
        dic['fcustomer_id'] = customerid
        dic['fdealer_id']   = self.dealerid
        tmp            = self.getVehicle(vid)
        dic            = dict(dic,**tmp)
        self.close_database()
        self.connect_database(2)
        common().insert('funnel_customer_roi',dic, self.cursor, self.db) 
        self.close_database()
        dic1 = {}
        dic1['sales']         = 0
        dic1['service']       = 1
        dic1['revenue']       = dic['invoiced']
        dic1['entrydate']     = dic['entrydate']
        return dic1 
    def insertSalesRoi(self,roi,customerid):
        self.connect_database()
        dic = {}
        dic['type'] = 1
        dic['entrydate'] = roi[common().getindex('sale','deal_date',self.cursor)] 
        dic['warrantyexpiration'] = roi[common().getindex('sale','warranty_exp_date',self.cursor)]
        dic['leaseexpiration'] = roi[common().getindex('sale','lease_exp_date',self.cursor)]
        dic['grossprofit'] = roi[common().getindex('sale','gross_profit_sale',self.cursor)]
        dic['new_used']    = roi[common().getindex('sale','new_used',self.cursor)]
        dic['deal_type']   = roi[common().getindex('sale','deal_type',self.cursor)]
        dic['sale_type']   = roi[common().getindex('sale','sale_type',self.cursor)]
        dic['standardized_deal_type']   = roi[common().getindex('sale','standardized_deal_type',self.cursor)]
        dic['fsales'] = roi[common().getindex('sale','slid',self.cursor)]
        vid            = roi[common().getindex('sale','vid',self.cursor)]
        tmp            = self.getVehicle(vid)
        dic            = dict(dic,**tmp)
        tmp            = self.getTrade(dic['fsales'])
        trd            = tmp
        dic            = dict(dic,**tmp)
        dic['fcustomer_id'] = customerid
        dic['fdealer_id']   = self.dealerid
        self.close_database()
        self.connect_database(2)
        common().insert('funnel_customer_roi',dic, self.cursor, self.db) 
        self.close_database()
        if trd['istradein'] == 1:
            if trd['tyear']!="":
                self.setTopVehicle(trd)
        dic1 = {}
        dic1['sales']         = 1
        dic1['service']       = 0
        dic1['revenue']       = dic['grossprofit']
        dic1['entrydate']     = dic['entrydate']
        return dic1         
    
    def insertLead(self,consumerid,sdata,type = 1):
        self.connect_database()
        sql = "select * from consumer where cid='%s' limit 1" % consumerid
        self.cursor.execute(sql)
        consumer = self.cursor.fetchone()
        self.close_database()   
        tmp  = {}
        dic  = {"fdealer_id":self.dealerid,"notificationcount":0,"consumerid":consumerid} 
        tmp  = dict(tmp,**dic)
        tmp1 = self.getname(consumer)
        tmp  = dict(tmp,**tmp1)
        tmp2 = self.getAddress(consumerid)
        tmp  = dict(tmp,**tmp2)
        tmp3 = self.getmail(consumerid)
        tmp  = dict(tmp,**tmp3)
        tmp4 = self.getroi(sdata,type)
        tmp  = dict(tmp,**tmp4)
        tmp5 = self.getPhone(consumerid)
        tmp  = dict(tmp,**tmp5)
        self.connect_database(2)
        leadid = common().insert('funnel_customer',tmp, self.cursor, self.db)
        keyid  = self.hashkey(str(leadid))
        common().update('funnel_customer',{"keyid":keyid},leadid,'id',self.cursor, self.db)
        self.close_database()
        return leadid
    def updateLead(self,customerid,sdata,type = 1):
        lead = self.getLeadInfo(customerid)
        roi  = self.getroi(sdata,type)
        lead['visit'] = lead['visit'] + 1
        if type == 1:
            lead['sales'] = lead['sales'] + 1
            if lead['last_sales_date'] is None:
               lead['last_sales_date'] = roi['lastvisit'] 
            elif lead['last_sales_date'] < roi['lastvisit']:
               lead['last_sales_date'] = roi['lastvisit']
            lead['grossprofit'] = float(lead['grossprofit']) + float(roi['grossprofit'])
        else:
            lead['service'] = lead['service'] + 1
            if lead['last_service_date'] is None:
               lead['last_service_date'] = roi['lastvisit'] 
            elif lead['last_service_date'] < roi['lastvisit']:
               lead['last_service_date'] = roi['lastvisit']
            lead['invoiced'] = float(lead['invoiced']) + float(roi['invoiced'])  
        if lead['lastvisit'] < roi['lastvisit']:
            lead['lastvisit'] = roi['lastvisit']
            lead['status']    = roi['status']
        id = lead['id']
        del lead['id']
        self.connect_database(2)
        common().update('funnel_customer',lead,id,'id',self.cursor,self.db)               
        self.close_database()
        return id         
    def setTozipcode(self,consumerid,type = 1):
        self.connect_database()
        sql = "select * from address where cid = %s limit 1" % consumerid
        self.cursor.execute(sql)
        if self.cursor.rowcount == 1:
            consumeraddress = self.cursor.fetchone()
            city  = consumeraddress[common().getindex('address','city',self.cursor)]
            state = consumeraddress[common().getindex('address','state',self.cursor)]
            zip   = consumeraddress[common().getindex('address','zip',self.cursor)]
            self.close_database()
            self.connect_database(2)
            sql = "select * from funnel_topzipcode where zip='%s' and city='%s' and state = '%s' and fdealer_id = '%s' limit 1" % (zip,city,state,self.dealerid)    
            self.cursor.execute(sql)
            if self.cursor.rowcount == 0:
                dict = {
                     "zip"        : zip,
                     "city"       : city,
                     "state"      : state,
                     "count"      : 1,
                     "sales"      : 0,
                     "service"    : 0,
                     "fdealer_id"   : self.dealerid
                    }
                if type == 1:
                    dict['sales']     = 1
                else:
                    dict['service']   = 1    
                common().insert('funnel_topzipcode',dict,self.cursor,self.db)
            else:
                    result = self.cursor.fetchone()
                    id     = result[0]
                    dict = {
                            "count"      : result[common().getindex('funnel_topzipcode','count', self.cursor)] + 1,
                            "sales"      : result[common().getindex('funnel_topzipcode','sales', self.cursor)],                
                            "service"    : result[common().getindex('funnel_topzipcode','service', self.cursor)],
                            }
                    if type == 1:
                        dict['sales']     = dict['sales'] + 1
                    else:
                        dict['service']   = dict['service'] + 1
                    common().update('funnel_topzipcode',dict,id,'id',self.cursor,self.db)               
        self.close_database()
    def processbysaleservice(self,n,type = 1):
        self.connect_database()
        if type == 1:
            cosumerid = n[common().getindex('sale','cid',self.cursor)]
        else:
            cosumerid = n[common().getindex('service','cid',self.cursor)]    
        self.close_database()
        if self.isConsumer(cosumerid) == False:
           leadid = self.insertLead(cosumerid,n,type)
        else:
           leadid = self.updateLead(cosumerid,n,type)
        if type == 1:
            roi = self.insertSalesRoi(n, leadid)
        else:
            roi = self.insertServiceRoi(n, leadid)
        #self.setTozipcode(cosumerid,type) 
        self.connect_database(2)
        roi['dealer'] = self.dealerid
        #hreport(self.db,self.cursor,roi,type).process()
        self.close_database()
        print cosumerid
        print leadid
        
            