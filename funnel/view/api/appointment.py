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
from dealerfunnel.funnel.model_plugin.yearmakemodel_model import yearmakemodel
class appointmentapi:
    
    def isset(self,variable):
        return variable in locals() or variable in globals()
    def setMongo(self):
        self.client           = MongoClient('localhost:27017')
        self.db               = self.client.funnel
    def getAppointment(self,request):
        cid = request.GET['cid']
        self.setMongo()
        leaddata = self.db.leaddata.find({"customerid":cid})[0]
        lead    = self.db.lead.find({"customerid":cid})[0]
        dict    = {}
        dict['customer']  = leaddata['customer']
        dict['trade']     = leaddata['trade']
        if lead['isapp']  == 0:
            dtetime       = datetime.datetime.now()
        dict['app']       = {"status":'Pending',"date":dtetime.strftime("%m-%d-%Y"),"time":dtetime.strftime("%I:%M %p")}
        dict['year']      = yearmakemodel().getYear()
        dict['make']      = yearmakemodel().getMake(dict['trade']['year'])
        dict['model']     = yearmakemodel().getModel(dict['trade']['year'],dict['trade']['make'])
        dict['state']     = yearmakemodel().getState()
        dict['appstatus'] = yearmakemodel().getAppStatus()    
        return HttpResponse(json.dumps(dict))                               