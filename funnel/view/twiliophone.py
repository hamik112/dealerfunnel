from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.library.twilio.rest import TwilioRestClient
from dealerfunnel.funnel.library.common import *
import datetime
class twiliophone():
    def __init__(self):
        self.menu     = 'Admin'
        self.submenu  = 'DEALERSHIP'
        self.sid      = "AC44b1c328110a5a6c78dece8ce7e2ebe6"
        self.token    = "838f32eceaf5c249cba6e6e8b89b7f9a"
        self.TestMode = False
        self.demosid  = 'Demo'  
    @csrf_exempt
    def callcenter(self,request):
        to = request.POST['To'][2:]
        s  = Twillio_phone.objects.filter(number = to)
        phone = ''
        if s.count() > 0:
            for item in s:
                id = item.id
            dealer = Dealer.objects.filter(ftwillio_id = id) 
            if dealer.count() > 0:
                for deal in dealer:
                    phone = deal.forwardnumber   
        return base(request).view_render('twiliophone/callcenter.html',{"phone":phone},self.menu,self.submenu,1)
        
    def searchbox(self,request):
        data = {}
        data["type"] = request.GET['id']
        if request.GET['id'] == 1:
            return base(request).view_render(Path().TWILLIO_SEARCHBOX,data,self.menu,self.submenu,1)
        else:
            return base(request).view_render(Path().TWILLIO_SEARCHBOX,data,self.menu,self.submenu,1)    
    def releasenumber(self,request):
        
        dealer  = Dealer.objects.get(id = int(request.GET['dealerid']))
        ftwillio = dealer.ftwillio
        if self.TestMode == False:       
           client = TwilioRestClient(self.sid,self.token)
           client.phone_numbers.delete(ftwillio.sid) 
        dealer.ftwillio = None
        dealer.save()
        ftwillio.delete()
        return HttpResponse('Done')
        
    def buynumberfromtwilio(self,number):
        client = TwilioRestClient(self.sid,self.token)
        number = client.phone_numbers.purchase(
                                            voice_url="http://dealerfunnel.com/twilio/callcenter/",
                                            phone_number='+1'+number,
                                            voice_method="POST"
                                            )
        return number.sid
    def buynumber(self,request):
        
        if self.TestMode:
            sid = 'demosid'     
        else:
            sid = self.buynumberfromtwilio(request.GET['number'])
        param   = ['number','city','state','zip']
        ext     = {"date":datetime.datetime.now().date(),"type":1,"sid":sid}
        dict    = commonfunction().parampack(param,request.GET,ext)  
        if request.GET['dealerid'] == '':
            obj= Twillio_phone(**dict)
            obj.save()
        else:    
            dealer  = Dealer.objects.get(id = int(request.GET['dealerid']))
            if dealer.ftwillio is None:
                obj= Twillio_phone(**dict)
                obj.save()
                dealer.ftwillio = obj
                dealer.save()
            else:
                for key,value in dict.iteritems():
                    setattr(dealer.ftwillio,key,value)
                dealer.ftwillio.save()
                obj = dealer.ftwillio
        jsondata                     = {}
        result                       = {}
        result['number']             = commonfunction().phone_formate(request.GET['number'],0)
        result['id']                 = obj.id
        jsondata['result']           = result
        return HttpResponse(json.dumps(jsondata))          
            
    def searchphone(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        
        mlist = ['','tollfree','local']
        sid = 'AC44b1c328110a5a6c78dece8ce7e2ebe6'
        token = '838f32eceaf5c249cba6e6e8b89b7f9a'
        client = TwilioRestClient(sid,token)
        dict = {"type":mlist[int(request.GET['type'])],"country":"US"}
        if request.GET['city']!='':
            dict['InRateCenter']= request.GET['city']
        if request.GET['pattern']!='':
            dict['contains']= request.GET['pattern']
        
        number = client.phone_numbers.search(**dict)
        nlist  = []
        i = 0
        for n in number:
            dict = {"number":n.phone_number,"type":request.GET['type'],"index":i}
            if n.rate_center is not None:
                dict['rate_center'] = n.rate_center
            else:
                dict['rate_center'] = ''
            if n.region is not None:
                dict['region'] = n.region
            else:
                dict['region'] = ''
            if n.postal_code is not None:
                dict['postal_code'] = n.postal_code
            else:
                dict['postal_code'] = ''
            nlist.append(dict)
            i = i + 1            
        jsondata           = {}
        jsondata['result'] = nlist
        return HttpResponse(json.dumps(jsondata))     
        
        
        
    