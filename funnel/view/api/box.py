from dealerfunnel.funnel.view.base import *
from django.core import serializers
import json
from dealerfunnel.funnel.library.dateformate import dateformateclass

class boxclass:
    def getCampaignBox(self,start,end):
        box = {"carsold":0,"grossprofit":0,"trades":0,"repairorders":0,"invoiced":0}
        obj = Campaign_roi_match.objects.filter(fcampaign = self.campaignObj).filter(entrydate__gte = start).filter(entrydate__lte = end)
        for n in obj:
            if n.type == 1:
                box['carsold']      = box['carsold'] + 1
            else:
                box['repairorders'] = box['repairorders'] + 1    
            box["grossprofit"] = box["grossprofit"] + n.grossprofit
            box["trades"] = box["trades"] + n.istradein
            box["invoiced"] = box["invoiced"] + n.invoiced
        return box
    def campaignbox(self,request):
        self.startDate = dateformateclass().date_obj(request.GET['startDate'])
        self.endDate   = dateformateclass().date_obj(request.GET['endDate'])
        self.keyid     = request.GET['keyid']
        
        
        