from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.analysis import *
from dealerfunnel.funnel.library.paginator_plugin import * 
from dealerfunnel.funnel.library.common import *
import csv
import datetime
def loginrequired(func):
   def func_wrapper(slf,request):
       if 'userinfo' in request.session:
           return  func(slf,request) 
       else:
           return HttpResponseRedirect(reverse('login_landing'))
       
   return func_wrapper
class reportroi():
    def __init__(self):
        self.menu    = ''
        self.submenu = ''
    
    def getreport(self,dealerid):
        query    = Campaign.objects.filter(fdealer = dealerid).values_list('trigger').order_by('trigger').distinct()
        mlist    = ['','Total Cusomers','Warranty Expiration','Crossover Conquest','Lease Expiration','Birthday','Equity Position','Trade Cycle','Make Conquest','Late Service']
        result   = []
        total    = {"Trigger":"Total","Campaigns":0,"MailPieces":0,"Email":0,"Leads":0,"CarsSold":0,"GrossProfit":0,
                     "RepairOrders":0,"ROTotal":0,"Cost":0,"ROI":0,"DaysActive":0
                   }
        now      = datetime.datetime.now().date()
        for n in query:
            slist = {"Trigger":"","Campaigns":0,"MailPieces":0,"Email":0,"Leads":0,"CarsSold":0,"GrossProfit":0,
                     "RepairOrders":0,"ROTotal":0,"Cost":0,"ROI":0,"DaysActive":0
                     }
            trigger = int(n[0])
            count   = Campaign.objects.filter(fdealer = dealerid).filter(trigger = trigger).count()
            if count > 0:
                slist["Campaigns"] = count
                total["Campaigns"] = total["Campaigns"] + count
                slist["Trigger"] = mlist[trigger]
                queryn  = Campaign.objects.filter(fdealer = dealerid).filter(trigger = trigger)
                for k in queryn:
                    if now >= k.startdate and now<= k.enddate:
                       slist["DaysActive"]      = 1  
                    slist["MailPieces"]         = slist["MailPieces"]   + k.totalmail
                    total["MailPieces"]         = total["MailPieces"]   + k.totalmail
                    slist["Email"]              = slist["Email"]        + k.totalemail
                    total["Email"]              = total["Email"]        + k.totalemail
                    slist["Cost"]               = slist["Cost"]         + k.totalcost
                    total["Cost"]               = total["Cost"]         + k.totalcost
                    slist["CarsSold"]           = slist["CarsSold"]     + 0
                    total["CarsSold"]           = total["CarsSold"]     + 0
                    slist["RepairOrders"]       = slist["RepairOrders"] + 0
                    total["RepairOrders"]       = total["RepairOrders"] + 0
                    slist["GrossProfit"]        = slist["GrossProfit"]  + 0
                    total["GrossProfit"]        = total["GrossProfit"]  + 0
                    slist["ROTotal"]            = slist["ROTotal"]      + 0
                    slist["Leads"]              = slist["Leads"]        + 0
                    total["Leads"]              = total["Leads"]        + 0
                    gains    = 0
                    cost     = k.totalcost
                    #roi      = (gains - cost) / cost
                    roi      = 0
                    slist["ROI"]                = slist["ROI"]  + roi
                    total["ROI"]                = total["ROI"]  + roi              
                slist["Cost"]                   = commonfunction().float_formate(slist["Cost"])
                slist["GrossProfit"]            = commonfunction().float_formate(slist["GrossProfit"])
                slist["ROTotal"]                = commonfunction().float_formate(slist["ROTotal"])
                slist["ROI"]                    = commonfunction().float_formate(slist["ROI"])
                result.append(slist)
        
        
        total["Cost"]               = commonfunction().float_formate(total["Cost"])
        total["GrossProfit"]        = commonfunction().float_formate(total["GrossProfit"])
        total["ROTotal"]            = commonfunction().float_formate(total["ROTotal"])
        total["ROI"]                = commonfunction().float_formate(total["ROI"])
        return [result,total]        
                     
    
    def downloadcsv(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        
        dealerid = request.GET['dealerid']
        report   = self.getreport(dealerid)[0]
        dealer   = Dealer.objects.get(id =dealerid)
        dealername = dealer.name.replace(" ", "_") + "_roireport.csv"
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + dealername
        writer = csv.writer(response)
        writer.writerow(['Trigger', 'Campaigns', 'Mail Pieces', 'Email','Leads','Cars Sold','Gross Profit','Repair Orders','RO Total','Cost','ROI','Days Active'])
        plist = ['Complete','In Progress']
        for n in report:
            mlist = []
            mlist.append(n['Trigger'])
            mlist.append(n['Campaigns'])
            mlist.append(n['MailPieces'])
            mlist.append(n['Email'])
            mlist.append(n['Leads'])
            mlist.append(n['CarsSold'])
            mlist.append(n['GrossProfit'])
            mlist.append(n['RepairOrders'])
            mlist.append(n['ROTotal'])
            mlist.append(n['Cost'])
            mlist.append(n['ROI'])
            mlist.append(plist[int(n['DaysActive'])])
            writer.writerow(mlist)
        return response
    @loginrequired        
    def landing(self,request):
        # This base function need to call for all url
        base(request).base_management(self.menu)
        self.menu    = 'ROI'
        return base(request).template_render(Path().REPORTS_ROI_LANDING,{},self.menu,self.submenu,1)
    def ajax(self,request):
        dealerid = request.GET['dealerid']
        report   = self.getreport(dealerid)
        return base(request).view_render(Path().REPORTS_ROI_AJAX,{"domain":Path().Domain,"dealerid":dealerid,"report":report[0],"total":report[1]},self.menu,self.submenu,1)
    @loginrequired
    def details(self,request):
        return base(request).template_render('report_roi/details.html',{},self.menu,self.submenu,1)                   