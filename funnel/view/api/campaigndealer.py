from django.core import serializers
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.library.common import *
from dealerfunnel.funnel.view.base import *
import json
import pdb
class api_campaigndealer:
    def getcampaignbydealer(self,dealerObj):
        todate = datetime.datetime.now().date()
        # Active Campaign
        dict                = {}
        active      = Campaign.objects.filter(fdealer = dealerObj).filter(startdate__lte = todate).filter(enddate__gte = todate)     
        old         = Campaign.objects.filter(fdealer = dealerObj).filter(enddate__lt = todate) 
        upcomming   = Campaign.objects.filter(fdealer = dealerObj).filter(startdate__gt = todate)
        activelst   = []
        alllst      = []
        for n in active:
            dct  = {}
            dct['name'] = n.name
            dct['id'] = n.id
            dct['key'] = n.keyid
            activelst.append(dct)
            alllst.append(dct)
        oldlst   = []
        for n in old:
            dct  = {}
            dct['name'] = n.name
            dct['id'] = n.id
            dct['key'] = n.keyid
            oldlst.append(dct)
            alllst.append(dct)
        upcomminglst   = []
        for n in upcomming:
            dct  = {}
            dct['name'] = n.name
            dct['id'] = n.id
            dct['key'] = n.keyid
            upcomminglst.append(dct)
            alllst.append(dct)        
        jsondata = {"Active":activelst,"Old":oldlst,"Upcomming":upcomminglst,"All":alllst}
        return   jsondata  
    def getallcampaignbydealer(self,request):
        key   = request.GET['id']
        dealerObj = Dealer.objects.get(keyid = key)
        jsondata = self.getcampaignbydealer(dealerObj)
        return HttpResponse(json.dumps(jsondata))    
    def getallcampaignbycmp(self,request):
        key    = request.GET['id']
        cmpObj = Campaign.objects.get(keyid = key)
        select = {"name":cmpObj.name,"id":cmpObj.id,"key":cmpObj.keyid}
        dealerObj  = cmpObj.fdealer
        jsondata = self.getcampaignbydealer(dealerObj)
        jsondata['selected'] = select
        return HttpResponse(json.dumps(jsondata)) 
     