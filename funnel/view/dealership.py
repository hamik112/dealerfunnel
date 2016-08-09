from dealerfunnel.funnel.view.base import *
import json
from dealerfunnel.funnel.model_plugin.cloudonesetting_model import *
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from dealerfunnel.funnel.models import *
def loginrequired(func):
   def func_wrapper(slf,request):
       if 'userinfo' in request.session:
           return  func(slf,request) 
       else:
           return HttpResponseRedirect(reverse('login_landing'))
       
   return func_wrapper
class dealership():
    def __init__(self):
        self.menu    = 'DEALERSHIP'
        self.submenu = ''
    @loginrequired
    def landing(self,request):
        # This base function need to call for all url
        base(request).base_management(self.menu)
        dealer = Dealer.objects.all()
        baseclass = base(request)
        baseclass.isdealerlist = 0
        return baseclass.template_render(Path().DEALERSHIP_LANDING,{"dealer":dealer},self.menu,self.submenu,1)
    @loginrequired
    def setup(self,request):
        state = State.objects.all() 
        city  = City.objects.all()
        mlist = []
        for n in city:
            mlist.append(n.city)
        citylist = json.dumps(mlist)     
        baseclass = base(request)
        baseclass.isdealerlist = 0
        return baseclass.template_render(Path().DEALERSHIP_SETUP,{"city":citylist,"state":state},self.menu,self.submenu,2)
    
    @loginrequired
    def delete_dealership(self,request):
        dealer   = Dealer.objects.get(keyid = request.GET['id']).delete()
        return HttpResponseRedirect(reverse('dealership_landing'))
    
    def __cloudonesetup(self,post,dealer):
        cloudoneparam = ['fd1','fd2','fd3','fd4','fd5','fd6','fd7','td1','td2','td3','td4','td5','td6','td7','id1','id2','id3','id4','id5','id6','id7','cname','time_zone','phone','gender','pronunciation','askfor','notes','script']
        dict          = {}
        for n in range(1,8):
            dict['fd'+str(n)] = '09:00 AM'
            dict['td'+str(n)] = '04:00 PM'
        for key,value in post.iteritems():
            if key in cloudoneparam:
                dict[key] = value
        cloudonesetting(dealer,dict).process()        
            
    def __editmarketrange(self,request):
        postinfo = request.POST.copy()
        dealerid = int(postinfo['dealerid'])
        dealer   = Dealer.objects.get(id = dealerid)
        editdistance = postinfo['outofmarketdistance']
        if editdistance!=dealer.outofmarketdistance:
            dealer.outofmarketdistance = editdistance
            dealer.save() 
            
            
    @loginrequired
    def editupload(self,request):
        self.__editmarketrange(request)
        postinfo = request.POST.copy()
        dealerid = int(postinfo['dealerid'])
        if 'rlogo' in request.FILES:
            postinfo['flogo']            = imageupload().set('rlogo',Path().DEALERSHIP_LOGO,request,Media_image())
        if 'mlogo' in request.FILES:
            postinfo['fmlogo']           = imageupload().set('mlogo',Path().DEALERSHIP_LOGO,request,Media_image())
        postinfo['sale_phone']       = commonfunction().phone_validation(str(postinfo['sale_phone']))
        postinfo['service_phone']    = commonfunction().phone_validation(str(postinfo['service_phone']))
        postinfo['trade_phone']      = commonfunction().phone_validation(str(postinfo['trade_phone']))
        postinfo['forwardnumber']    = commonfunction().phone_validation(postinfo['forwardnumber'])
        if postinfo['trigger_trade_cycle'] == '0':
           postinfo['triggers_email'] = 0 
        postinfo['zip']              =  postinfo['zip']  
        dealerinfo = Dealer.objects.get(id = dealerid)
        keyid      = dealerinfo.keyid   
        base_model().insert(dealerinfo,postinfo,2)   
        # Edit Total Cost On Campaign
        if dealerinfo.trigger_cost_per_pieces !=postinfo['trigger_cost_per_pieces']:
            costper = float(postinfo['trigger_cost_per_pieces'])
            campaign = Campaign.objects.filter(fdealer = dealerinfo)
            for n in campaign:
                n.totalcost = float(n.totalmail) * costper
                n.save()
        
        self.__cloudonesetup(postinfo,dealerinfo)
        url   = reverse('dealership_setup_edit') + '?id=' + keyid
        return HttpResponseRedirect(url)
    def __cloudonedata(self,dealer):
        try:
            Dealer_cloudone.objects.get(fdealer=dealer)
            dict = Dealer_cloudone.objects.filter(fdealer=dealer).values()[0]
        except ObjectDoesNotExist:
            dict = {'fd1':'09:00 AM','fd2':'09:00 AM','fd3':'09:00 AM','fd4':'09:00 AM','fd5':'09:00 AM','fd6':'09:00 AM','fd7':'09:00 AM','td1':'04:00 PM','td2':'04:00 PM','td3':'04:00 PM','td4':'04:00 PM','td5':'04:00 PM','td6':'04:00 PM','td7':'04:00 PM','id1':'1','id2':'1','id3':'1','id4':'1','id5':'1','id6':'1','id7':'1','cname':'','time_zone':'UTC','phone':'','gender':'M','pronunciation':'','askfor':'','notes':'','script':'502'}
        return dict
    @loginrequired                
    def editsetup(self,request):
        state = State.objects.all() 
        info     = Dealer.objects.get(keyid = request.GET['id'])
        baseclass = base(request)
        baseclass.isdealerlist = 0
        cloudone = self.__cloudonedata(info)
        return baseclass.template_render(Path().EDIT_DEALERSHIP_SETUP,{"domain":Path().Domain,"state":state,"info":info,"cloudone":cloudone},self.menu,self.submenu,2)
    @loginrequired     
    def jsondealerinfo(self,request):
        jsondata           = {}
        jsondata['dealer'] = Dealer.objects.filter(id=request.GET['dealer_id']).values('id','ftwillio_id')[0]
        return HttpResponse(json.dumps(jsondata))
    def configurearchive(self,dealer):
        from datetime import date, timedelta as td
        startdate = date(2008, 1, 1)
        enddate   = dateformateclass().getTodate()
        delta     = enddate - startdate
        for i in range(delta.days + 1):
            dt    = startdate + td(days=i)
            raw   = Customer_archive(date = dt,total = 0,active = 0,lessactive = 0,lost = 0,salesonly = 0,serviceonly =0,bothroi = 0, fdealer = dealer)
            raw.save()
    def setroi(self,dealer):
        from datetime import date
        obj       = Roiclient(dealerid = dealer.id,roi_id = dealer.csvfileid,sl='',sv='',flag = 0,lastupdate = date(2008, 1, 1))
        obj.save() 
    @loginrequired
    def setupform(self,request):
        # get all POST info
        postinfo = request.POST.copy() 
        # Upload Address Info 
        postinfo['zip']              = postinfo['zip']
        # Upload Image
        
        
        postinfo['flogo']            = imageupload().set('rlogo',Path().DEALERSHIP_LOGO,request,Media_image())
        postinfo['fmlogo']           = imageupload().set('mlogo',Path().DEALERSHIP_LOGO,request,Media_image())
        # Twilio Phone
        if postinfo['ftwilio'] == '':
            twl = None
        else:
            twl = Twillio_phone.objects.get(id=int(postinfo['ftwilio']))
        postinfo['ftwillio']         = twl
        postinfo['fsmstwillio']      = None
        
        postinfo['sale_phone']       = commonfunction().phone_validation(str(postinfo['sale_phone']))
        postinfo['service_phone']    = commonfunction().phone_validation(str(postinfo['service_phone']))
        postinfo['trade_phone']      = commonfunction().phone_validation(str(postinfo['trade_phone']))
        postinfo['forwardnumber']    = commonfunction().phone_validation(str(postinfo['forwardnumber']))
        
        lst = ['triggers_budget','triggers_pieces','trigger_cost_per_pieces']
        for n in lst:
            if postinfo[n] == '':
               postinfo[n] = 0  
        
        
        
        # Create Dealership Table
        dealer                       = base_model().insert(Dealer(),postinfo,2)
        keyid                        = base_model().setkeyid(dealer)
        dealerid = dealer.id
        ca = Customer_analysis(total_customer = 0,warrantyexpiration = 0,crossoverconquest = 0,leaseexpiration = 0,birthday = 0,euityposition= 0,tradecycle = 0,makeconquest = 0,lateservice = 0,fdealer_id = dealerid)
        ca.save()
        self.__cloudonesetup(postinfo,dealer)
        url                          = reverse('dealership_setup_edit') + '?id=' + keyid
        self.configurearchive(dealer)
        self.setroi(dealer)
        return HttpResponseRedirect(url)    
        
         
        
                   