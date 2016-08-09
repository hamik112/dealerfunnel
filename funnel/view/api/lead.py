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
class leadapi:
    
    def isset(self,variable):
        return variable in locals() or variable in globals()
    def setMongo(self):
        self.client           = MongoClient('localhost:27017')
        self.db               = self.client.funnel
    def param_setting(self,request):
        self.perpage = 50
        if 'start' in request.GET:
            self.startDate = dateformateclass().datetimefilter(request.GET['start'],1)
        if 'end' in request.GET:
            self.endDate = dateformateclass().datetimefilter(request.GET['end'],2)
        if 'dealer' in request.GET:
            self.dealerObj = Dealer.objects.get(keyid = request.GET['dealer'])
            self.dealerid  = self.dealerObj.id
        self.page = 1
        if 'page' in request.GET:
            self.page = int(request.GET['page'])
        if 'leadid' in request.GET:
            self.leadid = request.GET['leadid']
        self.isresponsetype = False
        if 'responsetype' in request.GET:
            responsetype =  request.GET['responsetype'].split(',')
            if responsetype[0] == '0':
                self.isresponsetype = False
            else:
                self.isresponsetype = True
                self.phoneresponse = 0
                self.webresponse   = 0
                self.appresponse   = 0
                for n in responsetype:
                    if n == '1':
                        self.phoneresponse = 1
                    if n == '2':
                        self.webresponse = 1
                    if n == '3':
                        self.appresponse = 1        
        self.islabel = False
        if 'label' in request.GET:
            labelid = int(request.GET['label'])
            if labelid>0:
                self.label = labelid
                self.islabel = True 
        self.istrigger = False
        if 'trigger' in request.GET:
            trigger =  request.GET['trigger'].split(',')
            if trigger[0] == '0':
                self.istrigger = False
            else:
                self.istrigger = True
                self.trigger = []
                for n in trigger:
                    self.trigger.append(int(n))
        self.iscampaign = False
        if 'campaign' in request.GET:
            cmp =  request.GET['campaign'].split(',')
            if cmp[0] == '0':
                self.iscampaign = False
            else:
                self.iscampaign = True
                self.cmpobj = []
                for n in cmp:
                    self.cmpobj.append(int(n)) 
        if 'sortcolum' in request.GET:
            self.sortorder = int(request.GET['sortorder'])
            self.sortcolum = int(request.GET['sortcolum'])    
        else:
            self.sortorder = 1
            self.sortcolum = 3
                                       
    def changeLabel(self,request):
        self.setMongo()
        leadObj  = request.GET['id']
        labelObj = request.GET['label']
        div  = {}
        div["label"] = int(labelObj)
        self.db.lead.update({"_id":ObjectId(leadObj)},{"$set":div})
        return HttpResponse('hi all')
    def getdaterange(self,request):
        jsondata = {}
        jsondata['start'] = '2015-11-28'
        jsondata['end'] = '2015-12-26'
        return HttpResponse(json.dumps(jsondata))
     
    def getFilter(self):
        filter = {}
        filter['dealer']   = self.dealerid
        filter['responsedate'] = { "$gte" : self.startDate,"$lte":self.endDate  }
        if self.iscampaign:
            filter['campaign'] = {"$in":self.cmpobj}
        if self.istrigger:
            filter['trigger'] = {"$in":self.trigger}
        if self.isresponsetype:
            if self.phoneresponse == 1:
               filter['isphone'] = 1
            if self.webresponse == 1:
               filter['isweb']  = 1
            if self.appresponse == 1:
               filter['isapp']  = 1         
        return filter    
    def setSession(self,request):
        param = {}
        param['dealer']            = self.dealerid
        param['startDate']         = self.startDate.strftime("%Y-%m-%d %H:%M:%S")
        param['endDate']           = self.endDate.strftime("%Y-%m-%d %H:%M:%S")
        param['iscampaign']        = self.iscampaign
        if self.iscampaign:
            param['campaign']          = self.cmpobj
        param['istrigger']         = self.istrigger
        if self.istrigger:
            param['trigger']           = self.trigger
        param['isresponsetype']    = self.isresponsetype
        if self.isresponsetype:
            param['phoneresponse']     = self.phoneresponse
            param['isweb']             = self.webresponse
            param['isapp']             = self.appresponse
        request.session['leadparam'] = param
        
    def getLead(self,request):
        self.setMongo()
        self.param_setting(request)
        filter    = self.getFilter()
        self.setSession(request)
        if self.islabel:
            filter['label'] = self.label
        count = self.db.lead.find(filter).count()
        pagin = commonfunction().pagination(self.page,count,50)
        sortlst = ['responsecount','fname','campaign_name','responsedate','lastvisitdate','label']
        orderlst = [pymongo.ASCENDING,pymongo.DESCENDING]
        obj   = self.db.lead.find(filter).sort(sortlst[self.sortcolum],orderlst[self.sortorder]).skip(pagin['offset']).limit(50)
        dict  = {}
        f = "%Y-%m-%d %H:%M:%S"
        responselst = []
        for n in obj:
            dict  = {}
            dict['name']           = commonfunction().isNoneStr(n['fname']) + ' ' + commonfunction().isNoneStr(n['lname'])
            dict['campaign']       = n['campaign_name']
            dict['label']          = n['label']
            dict['id']             = str(n['_id'])
            dict['cid']            = str(n['customerid'])
            dict['isnew']          = n['isnew']
            dict['label']          = n['label']
            dict['isweb']          = n['isweb']
            dict['isphone']        = n['isphone']
            dict['isapp']          = n['isapp']
            dict['notecount']      = n['notecount']
            dict['label']          = n['label']
            dict['lastdate']       = n['lastvisitdate'].strftime(f)
            dict['lastdateftime']  = dateformateclass().getTimeStamp(n['lastvisitdate'])
            dict['entrydate']      = n['responsedate'].strftime(f)
            dict['entrydateftime'] = dateformateclass().getTimeStamp(n['responsedate'])
            dst                    = commonfunction().getLabel(dict['label'])
            dict['icone']          = dst['icone']
            dict['iconeClass']     = dst['iconeClass']
            responselst.append(dict)
        jsondata  = {"lead":responselst}
        jsondata['count'] = count
        jsondata['totalpage'] = pagin['totalpage']
        jsondata['currentpage'] = self.page
        jsondata['start'] = pagin['start']
        jsondata['end'] = pagin['end']
        return HttpResponse(json.dumps(jsondata))    
    def getNewLead(self,request):
        self.setMongo()
        self.param_setting(request)
        filter    = self.getFilter()
        if self.islabel:
            filter['label'] = self.label
        filter['isnew'] = 1
        leadcount = self.db.lead.find(filter).count()
        jsondata  = {"newlead":leadcount}
        
        return HttpResponse(json.dumps(jsondata))   
    def getLeadCount(self,request):
        self.setMongo()
        self.param_setting(request)
        leadcount = self.db.lead.find(self.getFilter()).count()
        jsondata  = {"count":leadcount}
        return HttpResponse(json.dumps(jsondata))      
    def getResonponseLabel(self,request):
        self.setMongo()
        self.param_setting(request)
        label = self.db.lead.aggregate([{"$match":self.getFilter()},{"$group":{"_id":"$label","count":{"$sum":1}}}])
        labellst  = ['','Hot','Cold','Sold','Warm','Folloup','Dead']
        labeldict = {'Hot':0,'Cold':0,'Sold':0,'Warm':0,'Folloup':0,'Dead':0}
        newlead   = 0
        for n in label:
           labeldict[labellst[n['_id']]] =  n['count']
           
        jsondata     = {}
        jsondata['label']           = labeldict
        return HttpResponse(json.dumps(jsondata))
    def getCampaignList(self,request):
        self.param_setting(request)
        cmp = getcampaign().getcampaignbydaterange(self.dealerObj,self.startDate,self.endDate)
        lst = []
        for n in cmp:
           dict = {}
           dict['name'] = n.name
           dict['id'] = n.id
           dict['key'] = n.keyid
           lst.append(dict)
        jsondata     = {}
        jsondata['campaign']           = lst
        return HttpResponse(json.dumps(jsondata))   
    def adjustnewlead(self,request):
        self.setMongo()
        self.param_setting(request)
        self.db.lead.update_one({"_id":ObjectId(self.leadid)},{"$set":{"isnew":0}})
        return HttpResponse('Done')
    
    def updateleadatt(self,request):
        self.setMongo()
        idlst = request.GET['leadid'].split(',')
        att   = int(request.GET['att'])
        val   = int(request.GET['val'])
        attlst = ['','isnew','label','ownerid','isactive']
        updatekey = {}
        updatekey[attlst[att]] =  val
        if att == 3:
            if val>=0 :
                usr  = User.objects.get(id = val)
                updatekey['ownername'] =  usr.name
            else:
                updatekey['ownername'] =  'Undefine'    
        for n in idlst:
            self.db.lead.update_one({"_id":ObjectId(n)},{"$set":updatekey})
        
        jsondata = {}
        jsondata['status'] = 'ok'
        return HttpResponse(json.dumps(jsondata))
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
        self.db.customer_note.remove({"_id":ObjectId(id)})
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
           
                                   