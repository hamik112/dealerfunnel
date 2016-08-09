import MySQLdb
import math
from geocode import geocode
from datetime import datetime,timedelta
import hashlib
import time
from common import *
class campaign_roi_match:
    def __init__(self,db,cursor,roiid,customerid):
        self.db            = db
        self.cursor        = cursor
        self.roi           = roiid
        self.cid           = customerid
    def loadroi(self):
        sql   = "select * from funnel_customer_roi where id='%s' limit 1" % self.roi
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        dict   = {}
        dict["type"] = result[common().getindex('funnel_customer_roi','type',self.cursor)]
        dict["entrydate"] = result[common().getindex('funnel_customer_roi','entrydate',self.cursor)]
        dict["grossprofit"] = result[common().getindex('funnel_customer_roi','grossprofit',self.cursor)]
        dict["invoiced"] = result[common().getindex('funnel_customer_roi','invoiced',self.cursor)]
        dict["carsold"] = result[common().getindex('funnel_customer_roi','carsold',self.cursor)]
        dict['grossprofit'] = result[common().getindex('funnel_customer_roi','grossprofit',self.cursor)]
        dict['invoiced'] = result[common().getindex('funnel_customer_roi','invoiced',self.cursor)]
        dict['carsold'] = result[common().getindex('funnel_customer_roi','carsold',self.cursor)]
        dict['sales_delay'] = result[common().getindex('funnel_customer_roi','sales_delay',self.cursor)]
        dict['service_delay'] = result[common().getindex('funnel_customer_roi','service_delay',self.cursor)]
        dict['delay'] = result[common().getindex('funnel_customer_roi','delay',self.cursor)]
        dict['year'] = result[common().getindex('funnel_customer_roi','year',self.cursor)]
        dict['make'] = result[common().getindex('funnel_customer_roi','make',self.cursor)]
        dict['model'] = result[common().getindex('funnel_customer_roi','model',self.cursor)]
        dict['mileage'] = result[common().getindex('funnel_customer_roi','mileage',self.cursor)]
        dict['istradein'] = result[common().getindex('funnel_customer_roi','istradein',self.cursor)]
        dict['fdealer_id'] = result[common().getindex('funnel_customer_roi','fdealer_id',self.cursor)]    
        tmileage = result[common().getindex('funnel_customer_roi','tmileage',self.cursor)]
        if tmileage is None:
            dict['tmileage'] = 0  
        else:
            dict['tmileage'] = tmileage
        tyear = result[common().getindex('funnel_customer_roi','tyear',self.cursor)]
        if tyear is None:
               dict['tyear'] = 0
        else:
               dict['tyear'] = tyear 
        dict['tmake'] = result[common().getindex('funnel_customer_roi','tmake',self.cursor)]
        dict['tmodel'] = result[common().getindex('funnel_customer_roi','tmodel',self.cursor)]
        
        warrantyexpiration = result[common().getindex('funnel_customer_roi','warrantyexpiration',self.cursor)]
        if warrantyexpiration is None:
           dict['warrantyexpiration'] = '0000-00-00'
        else:
           dict['warrantyexpiration'] = warrantyexpiration
        leaseexpiration = result[common().getindex('funnel_customer_roi','leaseexpiration',self.cursor)]
        if leaseexpiration is None:
           dict['leaseexpiration'] = '0000-00-00'
        else:
           dict['leaseexpiration'] = leaseexpiration
        if int(dict["type"]) == 1: 
            dict["fsales_id"] = result[common().getindex('funnel_customer_roi','fsales_id',self.cursor)]
        else:
            dict["fservice_id"] = result[common().getindex('funnel_customer_roi','fservice_id',self.cursor)]
        dict["fcustomer_id"] = result[common().getindex('funnel_customer_roi','fcustomer_id',self.cursor)]
        self.roidata  = dict  
    def getcampaignlist(self):
        roi = self.roidata
        entrydate = roi['entrydate']
        cid       = self.cid
        sql = "select * from funnel_customer_campaign where fcustomer_id = '%s'" % cid
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        clist   = []
        for n in results:
            campaignid = n[2]
            sql1 = "select * from funnel_campaign where id='%s' limit 1" % campaignid
            self.cursor.execute(sql1)
            result = self.cursor.fetchone()
            startdate = result[common().getindex('funnel_campaign','startdate',self.cursor)]
            enddate = result[common().getindex('funnel_campaign','enddate',self.cursor)]
            if entrydate >= startdate and entrydate <= enddate:
                clist.append(campaignid)
        self.campaignlist = clist        
    def createroi(self):
        clist  = self.campaignlist
        roi    = self.roidata
        for n in clist:
            roi["fcampaign_id"] = n 
            common().insert('funnel_campaign_roi_match', roi,self.cursor,self.db)  
    def updateanalysis(self):
        clist  = self.campaignlist
        roi    = self.roidata
        for n in clist:
            sql = "select * from funnel_campaign where id='%s'" % n
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            analysisid = result[common().getindex('funnel_campaign','froi_id',self.cursor)]
            sql = "select * from funnel_campaign_roi_analysis where id='%s' limit 1" % analysisid
            self.cursor.execute(sql)
            result = self.cursor.fetchone()
            dict   = {}
            dict["car"] = int(result[common().getindex('funnel_campaign_roi_analysis','car',self.cursor)])
            dict["service"] = int(result[common().getindex('funnel_campaign_roi_analysis','service',self.cursor)])
            dict["grossprofit"] = (result[common().getindex('funnel_campaign_roi_analysis','grossprofit',self.cursor)])
            dict["invoiced"] = (result[common().getindex('funnel_campaign_roi_analysis','invoiced',self.cursor)])
            dict["carsold"] = (result[common().getindex('funnel_campaign_roi_analysis','carsold',self.cursor)])
            if int(roi["type"]) == 1:
                dict["car"] = dict["car"] + 1
                dict["grossprofit"] = dict["grossprofit"] + roi["grossprofit"]
                dict["carsold"] = dict["carsold"] + roi["carsold"]
            else:
                dict["invoiced"] = dict["invoiced"] + roi["invoiced"]
                dict["service"] = dict["service"] + 1    
            common().update('funnel_campaign_roi_analysis',dict,analysisid,'id',self.cursor,self.db)
    
    def process(self):
        self.loadroi()
        self.getcampaignlist()
        self.createroi()
        self.updateanalysis()

        
        
                                         