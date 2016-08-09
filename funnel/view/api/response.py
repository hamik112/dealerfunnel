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
class api_response:
    
    def isset(self,variable):
        return variable in locals() or variable in globals()
    def setMongo(self):
        self.client           = MongoClient('localhost:27017')
        self.db               = self.client.funnel
        
    def param_setting(self,request):
        if 'type' in request.GET:
            self.type  = int(request.GET['type'])
        if 'leadid' in request.GET:
            self.leadid = request.GET['leadid']
            self.leadObj = self.db.lead.find({"_id":ObjectId(self.leadid)})[0]
            self.leaddataObj = self.db.leaddata.find({"lead":ObjectId(self.leadid)})[0]
    def getresponseinfo(self,request):
        self.setMongo()
        self.param_setting(request)
        jsondata = {}
        jsondata['customer'] = self.leaddataObj['customer']
        jsondata['customerid'] = self.leaddataObj['customerid']
        jsondata['financialInfo'] = self.leaddataObj['financialInfo']
        jsondata['trade'] = self.leaddataObj['trade']
        jsondata['leadid'] = str(self.leaddataObj['lead'])
        jsondata['buytime'] = self.leaddataObj['buytime']
        jsondata['note'] = self.leaddataObj['note']
        jsondata['desiredvehicle'] = self.leaddataObj['desiredvehicle']
        response = self.leaddataObj['response']
        for n in response:
            if n['type'] == self.type:
               jsondata['response'] = n
        jsondata['response']["fdate"] = jsondata['response']['date'].strftime("%Y/%m/%d")        
        jsondata['response']["ftime"] = jsondata['response']['date'].strftime("%I:%M %p")
        jsondata['lead'] = self.leadObj
        jsondata['lead']['entrydate'] = dateformateclass().getdateformate(self.leadObj['entrydate'])
        jsondata['lead']['lastdate'] = dateformateclass().getdateformate(self.leadObj['lastdate'])
        jsondata['customer']['homephone'] = commonfunction().phone_formate(jsondata['customer']['homephone'],0)
        dst                    = commonfunction().getLabel(self.leadObj['label'])
        jsondata['icone']      = dst['icone']
        jsondata['iconeClass'] = dst['iconeClass']
        del jsondata['response']['date']
        del jsondata['lead']['_id']
        return HttpResponse(json.dumps(jsondata))
               
                          