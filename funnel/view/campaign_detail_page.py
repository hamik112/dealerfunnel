from dealerfunnel.funnel.view.base import *
from django.db.models import Q
import operator
import datetime
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.model_plugin.campaign_model import *
from dealerfunnel.funnel.model.campaign.campaigninfo import campaigninfo
from dealerfunnel.funnel.model.dealer.responsechart import responsechart
class campaigndetailpage():
    def __init__(self):
        self.menu    = 'CAMDP'
        self.submenu = ''
    
    
    def landing(self,request,dealerid,cmp):
        return base(request).template_render(Path().CMPDETAILPAGELANDING,{"dealerid":dealerid,"cmp":cmp},self.menu,self.submenu,1)
    
    def selected_campaign(self,request):
        dealerid     = int(request.GET['dealerid'])
        cmp          = Campaign.objects.get(keyid = request.GET['cmpid'])
        dealer       = Dealer.objects.get(id = dealerid)
        dealercmp    = Campaign.objects.filter(fdealer = dealer)
        end_date     = datetime.datetime.now().date()
        start_date   = end_date - datetime.timedelta(29)
        box          = campaigninfo().getcmpbox(cmp,start_date,end_date)
        response     = responsechart()
        response_chart = response.chartbycampaign(cmp.id)
        response_count = response.getCampaignCount(cmp.id,start_date,end_date)
        return base(request).view_render('campaign_detail_page/selected_campaign.html',{"start_date":start_date,"end_date":end_date,"cmp":cmp,"dealercmp":dealercmp,"dealerid":dealerid,"box":box,"response_chart":response_chart,"response_count":response_count},self.menu,self.submenu,1)
    def ajax_roi(self,request):
        start_date   = dateformateclass().date_obj(request.GET['startdate'],1)
        end_date     = dateformateclass().date_obj(request.GET['enddate'],1)
        cmp          = Campaign.objects.get(keyid = request.GET['cmpid'])
        roi          = campaigninfo().getRoi(cmp,start_date,end_date)
        leads        = campaigninfo().getLeads(cmp.id,start_date,end_date)
        return base(request).view_render('campaign_detail_page/ajax_roi.html',{"roi":roi,"leads":leads},self.menu,self.submenu,1)
     