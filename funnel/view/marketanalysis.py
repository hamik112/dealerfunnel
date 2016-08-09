from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.analysis import *
from dealerfunnel.funnel.library.paginator_plugin import * 
class marketanalysis():
    def __init__(self):
        self.menu    = ''
        self.submenu = ''
    def maintainfieldorder(self,field,order):
        type = ['','order1','order2','order3','order4','order5','order6'] 
        orderlist = ['sorting_desc','sorting_asc']
        list = {}
        list["order1"] = "sorting";
        list["order2"] = "sorting";
        list["order3"] = "sorting";
        list["order4"] = "sorting";
        list["order5"] = "sorting";
        list["order6"] = "sorting";
        list[type[field]] = orderlist[order]
        return list   
        
    def get_market_analysis(self,cpage,ptype,dealer,field,order):
        fieldorder  = [['','radious','customer','bns','snb','bs','makeconquest'],['','-radious','-customer','-bns','-snb','-bs','-makeconquest']]
        total  = Market_analysis.objects.filter(fdealer = dealer).exclude(radious = -1).count()
        pagin  = paginator_plugin(total,10,cpage,ptype).get()
        list   = {}
        list['analysis']  = Market_analysis.objects.filter(fdealer = dealer).exclude(radious = -1).order_by(fieldorder[order][field])[pagin['limit']:pagin['offset']]
        list['pagin']     = pagin
        return list    
    def ajax(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
                
        return base(request).view_render(Path().MALYSISAJAX,{},self.menu,self.submenu,1)
        
    def ajax_market_analysis_pagin(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        
        self.menu    = 'MARKETANALYSIS'
        dealerid     = request.GET['dealerid']
        cpage     = request.GET['cpage']
        tpage     = request.GET['tpage']
        fieldid   = request.GET['fieldid']
        orderid   = request.GET['orderid']
        customer_analysis = Customer_analysis.objects.get(fdealer = dealerid)
        analysis  = self.get_market_analysis(cpage,tpage,dealerid,int(fieldid),int(orderid))
        filedorder = self.maintainfieldorder(int(fieldid),int(orderid))
        return base(request).view_render(Path().MPAGINAJAX,{"filedorder":filedorder,"filedid":fieldid,"orderid":orderid,"market":analysis['analysis'],"pagin":analysis['pagin']},self.menu,self.submenu,1)
    @loginrequired     
    def landing(self,request):
        # This base function need to call for all url
        base(request).base_management(self.menu)
        self.menu    = 'MARKETANALYSIS'
        return base(request).template_render(Path().MARKETANALYSISLANDING,{},self.menu,self.submenu,1)
    def marketbreakdown(self,request):
        contentperpage = 20
        dealer    = int(request.GET['dealerid'])
        cpage     = int(request.GET['cpage'])
        sortorder = ['radious','bns','snb','bs']
        count     = Market_analysis.objects.filter(fdealer_id = dealer).count()
        pagin     = paginator_plugin(count,contentperpage,int(cpage),1).get()
        obj       = Market_analysis.objects.filter(fdealer_id = dealer).order_by(*sortorder)[pagin['limit']:pagin['offset']] 
        if cpage == 1:
            startcontent = 1
            endcontent   = contentperpage
        else:
            startcontent = ( contentperpage * (cpage - 1) ) + 1
            endcontent       = (contentperpage * cpage)
        if endcontent > pagin['total_content']:
            endcontent   =  pagin['total_content']   
                
        return base(request).view_render('marketanalysis/marketbreakdown.html',{"obj":obj,"pagin":pagin,"start":startcontent,"end":endcontent},self.menu,self.submenu,1) 
    def analysisbox(self,request):
        return base(request).view_render('marketanalysis/marketanalysis_box.html',{},self.menu,self.submenu,1) 
    def topzipcode(self,request):
        return base(request).view_render('marketanalysis/topzipcode.html',{},self.menu,self.submenu,1)                                       
    def toptradein(self,request):
        return base(request).view_render('marketanalysis/toptradein.html',{},self.menu,self.submenu,1)                                       