from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.library.paginator_plugin import * 
from django.db.models import Q
from datetime import datetime,timedelta
import pdb
from django.db import connection
import operator
class modal():
    def __init__(self):
        self.menu         = 'MODAL'
        self.submenu      = ''
    def customer(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        
        cid  = request.GET['cid']
        customer = Customer.objects.get(id = cid)
        isphone  = 0
        phone    = ''
        if customer.cellphone is not None:
            phone   = customer.cellphone
            isphone = 1
        elif customer.homephone is not None:
            phone   = customer.homephone
            isphone = 1
        elif customer.homephone is not None:
            phone   = customer.homephone
            isphone = 1        
        return base(request).view_render(Path().CUSTOMERMODAL,{"customer":customer,"phone":phone,"isphone":isphone},self.menu,self.submenu,1)
    def responsehtml(self,request):
        t = 100        