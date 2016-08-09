from dealerfunnel.funnel.view.base import *
from django.core import serializers
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.library.common import *
import json
import pdb
from dealerfunnel.funnel.library.dateformate import *
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q
import operator
import time
from django.db import connection
from dealerfunnel.funnel.model_plugin.campaign_model import *
from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo
class api_report:
    
    def isset(self,variable):
        return variable in locals() or variable in globals()
    def getsalesserviceinfo(self,ftype,dealerid):
        yearq    = Historical_report.objects.filter(fdealer = dealerid).filter(type = ftype).values_list('year').order_by('-year').distinct()
        yearlist  = []
        yearclist = []
        len = 0
        for n in yearq:
            len   = len + 1
            year  = int(n[0])
            query = Historical_report.objects.filter(fdealer = dealerid).filter(type = ftype).filter(year = year)
            i = 0
            revenue = 0
            for k in query:
                if ftype == 1:
                    i = i + k.sales
                else:
                    i = i + k.service    
                revenue = revenue + k.revenue
            dict = {"year":year,"number1":i,"number":commonfunction().numbergroup(i),"revenue":commonfunction().group(commonfunction().float_formate(revenue))}
            yearlist.append(dict)
            yearclist.append(dict)
        icon = ['fa-sort-up text-success','fa-sort-down text-danger','fa-sort']
        if len > 1:
            i = 0
            for n in yearlist:
                if i < len-1:
                    per         = commonfunction().percentage(n["number1"],yearlist[i+1]["number1"])
                    per["icon"] = icon[int(per["flag"])]
                    per["val"]  = commonfunction().float_formate(per["val"])     
                    n["per"]    = per
                else:
                    per         = {"val":0,"flag":0,"icon":"fa-sort"}    
                    n["per"]    = per    
                i = i + 1
        else:
            yearlist[0]["per"]  = {"val":0,"flag":0,"icon":"fa-sort"}        
        result = {"info":yearlist}
        year    = []
        chart_2 = []
        chart_3 = []
        chart_3.append('')
        i = 1
        yearclist.reverse()
        for n in yearclist:
            y  = []
            y.append(i)
            y.append(n["number1"])
            year.append(y)
            y  = []
            y.append(i)
            y.append(n["year"])
            chart_2.append(y)
            chart_3.append(str(n["revenue"]))
            i = i + 1
        result["year"] = year
        result["chart_2"] = chart_2
        result["chart_3"] = chart_3
        return result
    def getHistoricalSalesChart(self,request):
        data = self.getsalesserviceinfo(1,int(request.GET['dealerid']))
        return HttpResponse(json.dumps(data))
    def getHistoricalServiceChart(self,request):
        data = self.getsalesserviceinfo(2,int(request.GET['dealerid']))
        return HttpResponse(json.dumps(data))
    def getTopZipcode(self,request):
        dealerid       = int(request.GET['dealerid'])
        topz           = []
        Topzipcodeobj  = Topzipcode.objects.filter(fdealer = dealerid).order_by('-count')[:25]
        for n in  Topzipcodeobj:
            dict = {}
            dict['zip']  = n.zip
            dict['city'] = n.city
            dict['state'] = n.state
            dict['count'] = commonfunction().numbergroup(n.count)
            dict['sales'] = n.sales
            dict['service'] = n.service
            topz.append(dict)
        jsondata       = {}
        jsondata['topz'] = topz 
        return HttpResponse(json.dumps(jsondata))
    def gettoptradein(self,request):
        dealerid       = int(request.GET['dealerid'])
        Topvehicleobj  = Topvehicle.objects.filter(fdealer = dealerid).order_by('-count')[:25]
        topv           = []
        for n in Topvehicleobj:
            dict = {}
            dict['make'] = n.make
            dict['model'] = n.model
            dict['count'] = commonfunction().numbergroup(n.count)
            topv.append(dict)
        jsondata       = {}
        jsondata['topv'] = topv 
        return HttpResponse(json.dumps(jsondata))         
                          