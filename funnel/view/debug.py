from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.library.twilio.rest import TwilioRestClient
from dealerfunnel.funnel.library.mail import dealerfunnelmail
from django.template.loader import get_template
from django.core.mail import EmailMessage
import sys
from django.views.decorators.csrf import csrf_exempt
import pdb
import json
from dealerfunnel.funnel.model.lead.leadsetting import *
from dealerfunnel.funnel.model.lead.cloudleadsetting import *
from dealerfunnel.funnel.library.socialphoto import *
from dealerfunnel.funnel.model.customer.getinfo import *
from dealerfunnel.funnel.model.dealer.customeractivity_chart import *
from dealerfunnel.funnel.model.dealer.dashboard_chart import *
from dealerfunnel.funnel.model.campaign.campaigninfo import campaigninfo
from dealerfunnel.funnel.library.socialphoto import *
from dealerfunnel.funnel.model.cloudone.lead import *
import datetime
from dealerfunnel.funnel.model.note.notes import *

class debug():
    def __init__(self):
        self.menu    = 'Admin'
        self.submenu = 'DEALERSHIP'
    def getCustomerId(self,campaign):
        
        c = Customer_campaign.objects.filter(fcampaign_id = campaign).select_related()
        lst = []
        for n in c:
            lst.append(str(n.fcustomer.id))
        return lst
    
     
    
    
    def landing(self,request):
        cloaudonelead(100007933).setLead()
        return HttpResponse('Done')
        
    def testjquery(self,request):
        return base(request).view_render('debug/jquery.html',{},self.menu,self.submenu,1)
    def scanbarcode(self,request):
        now = datetime.datetime.now()
        html = "<html><body>It is now %s</body></html>" % now
        
        return HttpResponse(html)
        #return base(request).view_render('debug/scanbarcode.html',{},self.menu,self.submenu,1)
    @csrf_exempt
    def debugformsubmit(self,request):
        return HttpResponse('Hi all')   
    @csrf_exempt
    def checkbarcode(self,request):
        pin = int(request.POST['barcode'])
        customer = Customer.objects.get(barcode=pin)
        return base(request).view_render('debug/form.html',{'customer':customer},self.menu,self.submenu,1) 
    def customerdebug(self,request):
        cid = request.GET['cid']
        dict = {}
        dict['data'] = getcustomer(cid).dataPopulate()
        return HttpResponse(json.dumps(dict)) 
    def sangular(self,request):
        return base(request).view_render('debug/s1.html',{},self.menu,self.submenu,1) 
           