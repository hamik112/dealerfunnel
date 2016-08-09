from dealerfunnel.funnel.view.base import *
from django.core import serializers
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.library.common import *
import json
import pdb
from dealerfunnel.funnel.model_plugin.getcampaign_model import *
from dealerfunnel.funnel.model_plugin.getroi_model import *
from django.views.decorators.csrf import csrf_exempt
# Method - GET
# Param  - CampaignId,dateRange,type 
#
class callcenterapi:
    @csrf_exempt
    def center(self,request):
        to = request.POST['To']
        return HttpResponse(to)
        
             