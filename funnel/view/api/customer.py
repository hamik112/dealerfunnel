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
class customerapi:
    def setMongo(self):
        self.client           = MongoClient('localhost:27017')
        self.db               = self.client.funnel
    def getCustomer(self,request):
        cid  = request.GET['cid']
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
    def getresponseinfo(self,request):
        cid  = request.GET['cid']
        type = int(request.GET['type'])
        data = getcustomer(cid).dataPopulate()
        dict = {}
        dict['basic']           = data['Basic']
        dict['lead']            = data['Lead']
        if type == 1 or type == 2:
            dict['response']    = data['LastPhone']
        if type == 3:
            dict['response']    = data['LastWeb']
                
        return HttpResponse(json.dumps(dict))                           