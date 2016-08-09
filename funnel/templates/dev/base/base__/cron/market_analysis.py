import MySQLdb
from common import *
from datetime import datetime
class market_analysis:
    def __init__(self):
        self.db           = MySQLdb.connect('localhost','geoffkhalid','xD?i057j','admin_funnel')
        #self.db            = MySQLdb.connect('localhost','root','123456','dealerfunnel')
        self.cursor        = self.db.cursor()
    def radious(self,val):
        real_val  = float(val)
        int_val   = int(val)
        float_val = float(int_val)
        if real_val == float_val:
            return real_val
        else:
            return float_val + 1
    
    def unblockcron(self):
        dict = {"c1":0}
        common().update('funnel_cron',dict,2,'id',self.cursor,self.db)
            
    def isrun(self):
        sql = "select * from funnel_cron where id='2'"
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        if result[2] == 0:
            dict = {"c1":1}
            common().update('funnel_cron',dict,2,'id',self.cursor,self.db)
            return True
        else:
            return False 
    def analysis(self,data):
        sql = "select * from funnel_market_analysis_temp where fdealer_id='%s' and fzipcode_id='%s' and radious='%s' limit 1" % (data['dealer'],data['zip'],data['radious'])
        self.cursor.execute(sql)
        dict  = {}
        if self.cursor.rowcount == 0:
            dict["fzipcode_id"] = data["zip"]
            dict["radious"]  = data["radious"]
            dict["customer"]  = 1
            dict["city"]  = data["city"]
            dict["state"]  = data["state"]
            dict["makeconquest"]  = 0
            dict["salesmarketshare"]  = 0
            dict["crossoverconquest"]  = 0
            dict["fdealer_id"]  = data["dealer"]
            dict["bns"]      = 0
            dict["snb"]      = 0
            dict["bs"]       = 0 
            if data["service"] == 0:
               dict["bns"]     = 1
            if data["sales"] == 0:
               dict["snb"]     = 1
            if data["sales"] >= 1 and data["service"] >=1:
               dict["bs"]     = 1
            common().insert('funnel_market_analysis_temp', dict, self.cursor, self.db)
        else:
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            id     = result[0]
            dict   = {}
            dict["customer"] = result[common().getindex('funnel_market_analysis_temp','customer',self.cursor)] + 1                 
            if data["service"] == 0:
               dict["bns"]     = result[common().getindex('funnel_market_analysis_temp','bns',self.cursor)] + 1
            if data["sales"] == 0:
               dict["snb"]     = result[common().getindex('funnel_market_analysis_temp','snb',self.cursor)] + 1
            if data["sales"] >= 1 and data["service"] >=1:
               dict["bs"]     = result[common().getindex('funnel_market_analysis_temp','bs',self.cursor)] + 1
            common().update('funnel_market_analysis_temp',dict,id,'id',self.cursor,self.db)                       
            
    def swap(self):
        sql = "delete from funnel_market_analysis"
        self.cursor.execute(sql)
        sql = "select * from funnel_market_analysis_temp"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        for n in results:
            dict = {}
            dict["fzipcode_id"] = n[common().getindex('funnel_market_analysis_temp','fzipcode_id',self.cursor)]
            dict["radious"] = n[common().getindex('funnel_market_analysis_temp','radious',self.cursor)]
            dict["customer"] = n[common().getindex('funnel_market_analysis_temp','customer',self.cursor)]
            dict["city"] = n[common().getindex('funnel_market_analysis_temp','city',self.cursor)]
            dict["state"] = n[common().getindex('funnel_market_analysis_temp','state',self.cursor)]
            dict["bns"] = n[common().getindex('funnel_market_analysis_temp','bns',self.cursor)]
            dict["snb"] = n[common().getindex('funnel_market_analysis_temp','snb',self.cursor)]
            dict["bs"] = n[common().getindex('funnel_market_analysis_temp','bs',self.cursor)]
            dict["makeconquest"] = n[common().getindex('funnel_market_analysis_temp','makeconquest',self.cursor)]
            dict["salesmarketshare"] = n[common().getindex('funnel_market_analysis_temp','salesmarketshare',self.cursor)]
            dict["crossoverconquest"] = n[common().getindex('funnel_market_analysis_temp','crossoverconquest',self.cursor)]
            dict["fdealer_id"] = n[common().getindex('funnel_market_analysis_temp','fdealer_id',self.cursor)]
            common().insert('funnel_market_analysis', dict, self.cursor, self.db)
    
    def process(self):
        sql = "delete from funnel_market_analysis_temp"
        self.cursor.execute(sql)
        sql = "select * from funnel_customer"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        dict ={"zip":"","radious":"","city":"","state":"","dealer":"","sales":"","service":""}
        for n in results:
            dict["zip"]       = n[common().getindex('funnel_customer','fzip_id',self.cursor)]
            dict["radious"]   = self.radious(n[common().getindex('funnel_customer','distance',self.cursor)])
            dict["city"]      = n[common().getindex('funnel_customer','city',self.cursor)]
            dict["state"]     = n[common().getindex('funnel_customer','state',self.cursor)]
            dict["dealer"]    = n[common().getindex('funnel_customer','fdealer_id',self.cursor)]
            dict["sales"]       = n[common().getindex('funnel_customer','sales',self.cursor)]
            dict["service"]       = n[common().getindex('funnel_customer','service',self.cursor)]
            self.analysis(dict)
    def run(self):
        time1 = datetime.now()
        if self.isrun():
           self.process()
           self.swap()
           self.unblockcron()
        time2 = datetime.now()    
        print (time2-time1)        
market_analysis().run()
        