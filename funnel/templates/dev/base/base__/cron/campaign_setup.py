import MySQLdb
import math
from datetime import datetime
import time
from common import *
db  = MySQLdb.connect('205.186.143.147','geoffkhalid','xD?i057j','admin_funnel')
cursor = db.cursor()
time1 = datetime.now()
sql = "select * from funnel_cron_campaign_build limit 1"
cursor.execute(sql)
if cursor.rowcount > 0:
    flag = 0
    if flag == 0:
        sql1 = "select * from funnel_cron_campaign_build where 1 limit 1"
        cursor.execute(sql1)
        result = cursor.fetchone()
        campaign = result[common().getindex('funnel_cron_campaign_build','campaign',cursor)]
        customer = result[common().getindex('funnel_cron_campaign_build','customer',cursor)]
        sdate    = result[common().getindex('funnel_cron_campaign_build','sdate',cursor)]
        ndate    = result[common().getindex('funnel_cron_campaign_build','ndate',cursor)]
        cron_id  = result[0]
        c        = customer.split(',')
        roidict  = {"car":0,"service":0,"grossprofit":0,"invoiced":0,"carsold":0}
        sql4     = "select * from funnel_campaign where id='%s' limit 1" % campaign
        cursor.execute(sql4)
        result4 = cursor.fetchone()
        froi_id    = result4[common().getindex('funnel_campaign','froi_id',cursor)]
        for n in c:
            sql3 = "select * from funnel_customer_roi where fcustomer_id = '%s' and entrydate>='%s' and entrydate<='%s'" % (n,sdate,ndate)   
            cursor.execute(sql3)
            results = cursor.fetchall()
            for s in results:
                dict = {}
                dict['type'] = s[common().getindex('funnel_customer_roi','type',cursor)]
                type         = int(dict['type'])
                if type == 1:
                    roidict["car"] = roidict["car"] + 1 
                else:
                    roidict["service"] = roidict["service"] + 1    
                dict['entrydate'] = s[common().getindex('funnel_customer_roi','entrydate',cursor)]
                dict['grossprofit'] = s[common().getindex('funnel_customer_roi','grossprofit',cursor)]
                dict['invoiced'] = s[common().getindex('funnel_customer_roi','invoiced',cursor)]
                dict['carsold'] = s[common().getindex('funnel_customer_roi','carsold',cursor)]
                dict['entrydate'] = s[common().getindex('funnel_customer_roi','entrydate',cursor)]
                warrantyexpiration = s[common().getindex('funnel_customer_roi','warrantyexpiration',cursor)]
                if warrantyexpiration is None:
                    dict['warrantyexpiration'] = '0000-00-00'
                else:
                    dict['warrantyexpiration'] = warrantyexpiration
                leaseexpiration = s[common().getindex('funnel_customer_roi','leaseexpiration',cursor)]
                if leaseexpiration is None:
                    dict['leaseexpiration'] = '0000-00-00'
                else:
                    dict['leaseexpiration'] = leaseexpiration
                dict['grossprofit'] = s[common().getindex('funnel_customer_roi','grossprofit',cursor)]
                dict['invoiced'] = s[common().getindex('funnel_customer_roi','invoiced',cursor)]
                dict['carsold'] = s[common().getindex('funnel_customer_roi','carsold',cursor)]
                dict['sales_delay'] = s[common().getindex('funnel_customer_roi','sales_delay',cursor)]
                dict['service_delay'] = s[common().getindex('funnel_customer_roi','service_delay',cursor)]
                dict['delay'] = s[common().getindex('funnel_customer_roi','delay',cursor)]
                dict['year'] = s[common().getindex('funnel_customer_roi','year',cursor)]
                dict['make'] = s[common().getindex('funnel_customer_roi','make',cursor)]
                dict['model'] = s[common().getindex('funnel_customer_roi','model',cursor)]
                dict['mileage'] = s[common().getindex('funnel_customer_roi','mileage',cursor)]
                dict['fdealer_id'] = s[common().getindex('funnel_customer_roi','fdealer_id',cursor)]
                tyear = s[common().getindex('funnel_customer_roi','tyear',cursor)]
                if tyear is None:
                   dict['tyear'] = 0
                else:
                   dict['tyear'] = tyear  
                dict['tmake'] = s[common().getindex('funnel_customer_roi','tmake',cursor)]
                dict['tmodel'] = s[common().getindex('funnel_customer_roi','tmodel',cursor)]
                tmileage = s[common().getindex('funnel_customer_roi','tmileage',cursor)]
                if tmileage is None:
                   dict['tmileage'] = 0
                else:
                   dict['tmileage'] = tyear
                dict['istradein'] = s[common().getindex('funnel_customer_roi','istradein',cursor)]
                dict['fcustomer_id'] = s[common().getindex('funnel_customer_roi','fcustomer_id',cursor)]
                roidict["grossprofit"] = dict["grossprofit"] +  roidict["grossprofit"]
                roidict["invoiced"] = dict["invoiced"] +  roidict["invoiced"]
                roidict["carsold"] = dict["carsold"] +  roidict["carsold"]
                if type == 1:
                    dict['fsales_id'] = s[common().getindex('funnel_customer_roi','fsales_id',cursor)]
                else:
                    dict['fservice_id'] = s[common().getindex('funnel_customer_roi','fservice_id',cursor)]
                dict['fcampaign_id'] = campaign
                dict['fcustomer_id'] = s[common().getindex('funnel_customer_roi','fcustomer_id',cursor)]
                common().insert('funnel_campaign_roi_match',dict,cursor,db)
            sql2 = "select * from funnel_customer where id = '%s' limit 1" % n
            
            cursor.execute(sql2)
            result = cursor.fetchone()
            cid    = result[0]
            notification  = int(result[common().getindex('funnel_customer','notificationcount',cursor)]) + 1
            dict = {}
            dict["fcampaign"] = campaign
            dict["notificationcount"] = notification
            dict["lastnotification"] = ndate
            
            common().update('funnel_customer',dict,cid,'id',cursor,db)
            dict = {}
            dict['fcustomer_id'] = cid
            dict['fcampaign_id'] = campaign
            common().insert('funnel_customer_campaign', dict,cursor,db)  
        
        common().update('funnel_campaign_roi_analysis',roidict,froi_id,'id',cursor,db)
        
        sql1  = "delete from funnel_cron_campaign_build where id='%s'" % cron_id
        cursor.execute(sql1) 
        db.commit()
          
    
time2 = datetime.now()

print time2 - time1        
    
    
    
    
