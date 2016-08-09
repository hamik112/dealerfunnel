from dealerfunnel.funnel.view.base import *
from django.db.models import Q
import operator
import datetime
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.model_plugin.campaign_model import *
from dealerfunnel.funnel.model.campaign.getcampaignbydealer import *
from dealerfunnel.funnel.model.campaign.campaignroi import *
from dealerfunnel.funnel.model.campaign.box import campaignbox
from dealerfunnel.funnel.model.campaign.campaigninfo import campaigninfo
def loginrequired(func):
   def func_wrapper(slf,request):
       if 'userinfo' in request.session:
           return  func(slf,request) 
       else:
           return HttpResponseRedirect(reverse('login_landing'))
       
   return func_wrapper
class campaign():
    def __init__(self):
        self.menu    = 'CAMPAIGN'
        self.submenu = ''
    @loginrequired
    def landing(self,request):
        # This base function need to call for all url
        base(request).base_management(self.menu)
        return base(request).template_render(Path().CMP_LANDING,{},self.menu,self.submenu,1)
    @loginrequired
    def load_by_ajax(self,request):
        
        start_date   = dateformateclass().date_obj(request.GET['startdate'],1)
        end_date     = dateformateclass().date_obj(request.GET['enddate'],1)
        dealerid     = int(request.GET['dealerid'])
        dealer       = Dealer.objects.get(id = dealerid)
        cmp = campaigninfo().getcmpbydealer(int(dealerid),start_date,end_date)
        compare_cmp = campaigninfo().getCompareBox(cmp,int(dealerid),start_date,end_date)
        return base(request).view_render(Path().CAMPAIGN_AJAX_LOAD,{"dealer":dealer,"cmp":cmp,"compare_cmp":compare_cmp},self.menu,self.submenu,1)
    @loginrequired
    def load_by_dealer(self,request):
        enddate = datetime.datetime.now().date()
        startdate = enddate - datetime.timedelta(29) 
        return base(request).view_render(Path().CAMPAIGN_DEALER_LOAD,{"enddate":enddate,"startdate":startdate},self.menu,self.submenu,1)
    @loginrequired
    def status_change(self,request):
        cid = request.GET['cid']
        sentstatus = request.GET['status']
        Campaign.objects.filter(id = cid).update(status = sentstatus)
        mlist = ['','Execute','Scheduled']
        str = "<span  onclick=\"openmodal(" + sentstatus + "," + cid + ")\" class=\"label label-success cursor_style\">" + mlist[int(sentstatus)] + "</span>"
        return HttpResponse(str)
    @loginrequired
    def dealership_setup_budget_filter(self,request):
        dealerid =   int(request.GET['id'])
        key               = Dealer.objects.get(id = dealerid)
        budgetmonth = request.GET['budget'].split(",")
        smonth      = request.GET['budget']
        mlist = ['p0','p1','p2','p3','p4','p5','p6','p7','p8','p9','p10','p11','p12']
        month = {'p0':0,'p1':0,'p2':0,'p3':0,'p4':0,'p5':0,'p6':0,'p7':0,'p8':0,'p9':0,'p10':0,'p11':0,'p12':0}
        
        if budgetmonth[0] == '0':
            campaign          = Campaign.objects.filter(fdealer = dealerid)
            month['p0']    = 1
        else:
            query          = Campaign.objects.filter(fdealer = dealerid)
            mylist         = []
            for n in  budgetmonth:
                month[mlist[int(n)]] = 1
                mylist.append(Q(budgetmonth = int(n))) 
            campaign = query.filter(reduce(operator.or_, mylist))
        topbox            = {"total":0,"Cost":0,"Carsold":0,"GrossProfit":0,"RepairOrders":0,"ROTotal":0}
        for n in campaign:
            topbox["total"] = topbox["total"] + 1
            topbox["Cost"]  = topbox["Cost"] + n.totalcost
            topbox["Carsold"]  = topbox["Carsold"] + n.froi.car
            topbox["GrossProfit"]  = topbox["GrossProfit"] + n.froi.grossprofit
            topbox["RepairOrders"]  = topbox["RepairOrders"] + n.froi.service
            topbox["ROTotal"]  = topbox["ROTotal"] + n.froi.invoiced
        return base(request).view_render(Path().DEALERSHIP_SETUP_CMP_BUDGETMONTH,{"smonth":smonth,"month":month,"dealer":key,"campaign":campaign,"keyid":id,"topbox":topbox},self.menu,self.submenu,1)                
    @loginrequired
    def dealership_setup(self,request):
        base(request).base_management(self.menu) 
        month = int(datetime.datetime.now().strftime("%m"))
        id                = request.GET['id']
        dealer            = Dealer.objects.get(keyid = id)
        key               = id
        cmp = campaignbydealer(dealer.id,None,None,None).process()
        box = campaignbox().getSingleBox(cmp)
        return base(request).template_render(Path().DEALERSHIP_SETUP_CMP,{"domain":Path().Domain,"month":month,"dealer":key,"campaign":cmp,"box":box},self.menu,self.submenu,1)          