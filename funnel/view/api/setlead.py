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
from django.views.decorators.csrf import csrf_exempt
from dealerfunnel.funnel.model_plugin.getcustomer_model import *
from dealerfunnel.funnel.model_plugin.response_setting_mongo import *
import datetime
class setleadapi:
    def setMongo(self):
        self.client           = MongoClient('localhost:27017')
        self.db               = self.client.funnel
    
    @csrf_exempt
    def setApp(self,request):
        param = json.loads(request.body)
        islead = int(param['islead'])
        isapp  = int(param['isapp'])
        cid    = param['cid']
        
        response = {}
        response['customerObj']     = Customer.objects.get(keyid = cid)
        response['labelObj']        = 1
        response['responsetypeObj'] = 4
        response['sourceObj']       = ''
        response['call']            = {}
        response['agent']           = 'Khalid'
        response['date']            = datetime.datetime.now()
        
        app                         = {}
        app['appdatetime']          = dateformateclass().appdatetime_obj(param['date'],param['time'])      
        app['appstatus']            = param['status']
        response['app']             = app
        
        basicinfo                   = {}
        if 'homephone' in param:
            basicinfo['homephone']  = commonfunction().phone_validation(param['homephone'])
        else:
            basicinfo['homephone']  = '' 
        if 'workphone' in param:
            basicinfo['workphone']      = commonfunction().phone_validation(param['workphone'])
        else:
            basicinfo['workphone']  = ''
        if 'email' in param:
            basicinfo['email']      = param['email']
        else:
            basicinfo['email']      = ''    
        
        leadsetting                 = response_setting_mongo(response)
        
        if islead == 1:
            if isapp == 1:
                leadsetting.updateApp(param['appid'])
            else:
                leadsetting.setResponse()       
        else:
            leadsetting.setResponse()    
        
        leadsetting.updateBasicInfo(basicinfo)
        
        data = getcustomer(cid).dataPopulate()
        dict = {}
        dict['basic']           = data['Basic']
        dict['extra']           = data['Extra']
        dict['note']            = data['Note']
        dict['appointment']     = data['Appointment']
        dict['Response']        = data['Response']
        dict['isCampaign']      = data['isCampaign']
        dict['lookup']          = data['Lookup']
        dict['isLead']          = data['isLead']
        dict['id']              = data['Id']
        dict['isApp']           = data['isApp']
        return HttpResponse(json.dumps(dict))     
            
               