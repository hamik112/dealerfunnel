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
class customernoteapi:
    
    def isset(self,variable):
        return variable in locals() or variable in globals()
    def setMongo(self):
        self.client           = MongoClient('localhost:27017')
        self.db               = self.client.funnel
    def updateNotecount(self,cid,flag):
        lead = self.db.lead.find({"customerid":cid})[0]
        count = int(lead['notecount'])
        if flag == 1:
            count = count + 1
        else:
            count = count - 1
        self.db.lead.update_one({"customerid":cid},{"$set":{"notecount":count}})        
    def getNote(self,cid):
        self.setMongo()
        key = {"cid":cid}
        note = self.db.customer_note.find(key).sort('date',pymongo.DESCENDING)
        data = []
        for n in note:
            dict = {}
            dict['note']  = n['note']
            dict['id']    = str(n['_id'])
            dict['agent'] = n['agent']
            dict['date']  = n['date'].strftime("%b %d %Y %I:%M %p")
            data.append(dict)
        return data    
    def getnotes(self,request):
        jsondata = {}
        jsondata['note'] = self.getNote(request.GET['cid'])
        return HttpResponse(json.dumps(jsondata))
    def deletenotes(self,request):
        self.setMongo()
        id = request.GET['id']
        lead = self.customer_note.find({"_id":ObjectId(id)})[0]
        self.db.customer_note.remove({"_id":ObjectId(id)})
        self.updateNotecount(lead['cid'],0)
        jsondata = {}
        jsondata['note'] = self.getNote(request.GET['cid'])
        return HttpResponse(json.dumps(jsondata))
          
    @csrf_exempt
    def addnote(self,request):
        self.setMongo()
        param = json.loads(request.body)
        cid   = param['cid']
        note  = param['note']
        data  = {}
        data['cid']   = cid
        data['note']  = note
        data['agent'] = base(request).getUserName()
        data['date']  = dateformateclass().getNow()
        self.db.customer_note.insert_one(data)
        note = self.getNote(cid)
        self.updateNotecount(cid,1)
        jsondata = {}
        jsondata['note'] = note
        return HttpResponse(json.dumps(jsondata))
    @csrf_exempt
    def updatenote(self,request):
        self.setMongo()
        param = json.loads(request.body)
        id   = param['id']
        note  = param['note']
        self.db.customer_note.update_one({"_id":ObjectId(id)},{"$set":{"note":note}})
        jsondata = {}
        jsondata['status'] = 'ok'
        return HttpResponse(json.dumps(jsondata))    
           
                                   