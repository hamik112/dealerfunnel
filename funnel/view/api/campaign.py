from dealerfunnel.funnel.view.base import *
from django.core import serializers
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.library.common import *
import json
import pdb
from dealerfunnel.funnel.model_plugin.getcampaign_model import *
from dealerfunnel.funnel.model_plugin.getroi_model import *
# Method - GET
# Param  - CampaignId,dateRange,type 
#
class campaignapi:
    def getroimatch(self,request):
        jsondata = getroi().getroimatch(request.GET['startDate'],request.GET['endDate'],request.GET['id'])            
        return HttpResponse(json.dumps(jsondata))
           
    def campaignbox(self,request):
        dict     = getroi().campaignbox(request.GET['startDate'], request.GET['endDate'], request.GET['keyid'])
        return HttpResponse(json.dumps(dict))
    
    def getstats(self,request):
        cid          = request.GET['keyid']
        cmp          = Campaign.objects.get(keyid=cid)
        jsonData     = getcampaign(cmp.id).getstarts()
        return HttpResponse(json.dumps(jsonData))   
    def response_count(self,request):
        cid          = request.GET['keyid']
        cmp          = Campaign.objects.get(keyid=cid)
        jsonData     = getcampaign(cmp.id).getChart()
        return HttpResponse(json.dumps(jsonData))
    def getDate(self,request):
        cid          = request.GET['keyid']
        cmp          = Campaign.objects.get(keyid=cid)
        dict         = {}
        dict['startdate'] = cmp.startdate.strftime("%Y-%m-%d")
        dict['enddate']   = cmp.enddate.strftime("%Y-%m-%d")
        return HttpResponse(json.dumps(dict))
             