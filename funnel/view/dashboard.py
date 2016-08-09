from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.campaign_model import *
from django.core.urlresolvers import reverse
from django.db.models import Sum
from dealerfunnel.funnel.model.dashboard.dashboard_customer import *
from dealerfunnel.funnel.model.dealer.dashboard_chart import *
from dealerfunnel.funnel.model.dealer.dashboard_activity import *
from dealerfunnel.funnel.model.campaign.getcampaignbydealer import *
from dealerfunnel.funnel.model.campaign.campaignroi import *
from dealerfunnel.funnel.model.campaign.box import campaignbox
from dealerfunnel.funnel.model.campaign.campaigncampare import campaigncompare
from dealerfunnel.funnel.model.dealer.responsechart import responsechart
from dealerfunnel.funnel.model.campaign.campaigninfo import campaigninfo
class dashboard():
    def __init__(self):
        self.menu    = 'DASHBOARD'
        self.submenu = ''
    
    @loginrequired    
    def landing(self,request):
        
        base(request).base_management(self.menu)
        return base(request).template_render(Path().DASH_LANDING,{},self.menu,self.submenu,1)
    
    def dealerpage(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        
        # Start Date and End Date
        end_date     = datetime.datetime.now().date()
        start_date   = end_date - datetime.timedelta(29) 
        
        # Previous Date Slot
        pdate        = dateformateclass().backdate(start_date, end_date)
        dealerid     = request.GET['dealerid']
        dealer       = Dealer.objects.get(id = int(dealerid))
        dic      = {}
        dic['compare'] = dashboardcustomer(dealerid).getCompareResult()
        dic['status'] = dashboardcustomer(dealerid).getStatus()
        chart = dashboardchart(1,dealerid).run()
        activity = dashboardactivity(dealerid,1).process()
        cmp = campaigninfo().getcmpbydealer(int(dealerid),start_date,end_date)
        compare_cmp = campaigninfo().getCompareBox(cmp,int(dealerid),start_date,end_date)
        response    = responsechart()
        response_chart = response.chartbydealer(int(dealerid))
        response_count = response.getCount(int(dealerid),start_date,end_date)
        return base(request).view_render(Path().DASH_DEALERPAGE,{"response_chart":response_chart,"response_count":response_count,"chart":chart,"customer_part":dic,"activity":activity,"dealer":dealer,"cmp":cmp,"compare_cmp":compare_cmp},self.menu,self.submenu,1)
    
    def ajax_chart(self,request):
        dealerid     = int(request.GET['dealerid'])
        maptype      = int(request.GET['maptype'])
        chart = dashboardchart(maptype,dealerid).run()
        activity = dashboardactivity(dealerid,maptype).process()
        return base(request).view_render('dashboard/ajax_chart.html',{"activity":activity,"chart":chart},self.menu,self.submenu,1)
        
    def ajax_customer_compare(self,request):
        start_date   = dateformateclass().date_obj(request.GET['start_date'],2)
        end_date     = dateformateclass().date_obj(request.GET['end_date'],2)
        dealerid     = request.GET['dealerid']
        dic      = {}
        dic['compare'] = dashboardcustomer(dealerid).getCompareResult(start_date,end_date)
        return base(request).view_render('dashboard/ajax_customer_compare.html',{"customer_part":dic},self.menu,self.submenu,1)
    def datefilter(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        start_date   = dateformateclass().date_obj(request.GET['startdate'],1)
        end_date     = dateformateclass().date_obj(request.GET['enddate'],1)
        dealerid     = request.GET['dealerid']
        cmp = campaigninfo().getcmpbydealer(int(dealerid),start_date,end_date)
        compare_cmp = campaigninfo().getCompareBox(cmp,int(dealerid),start_date,end_date)
        response    = responsechart()
        response_chart = response.chartbydealer(int(dealerid))
        response_count = response.getCount(start_date,end_date)
        dealer       = Dealer.objects.get(id = int(dealerid))
        return base(request).view_render(Path().DASH_DATEFILER,{"dealer":dealer,"response_chart":response_chart,"response_count":response_count,"cmp":cmp,"compare_cmp":compare_cmp},self.menu,self.submenu,1)
    
        