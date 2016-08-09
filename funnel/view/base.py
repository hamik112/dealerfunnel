from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader ,Context, Template
from django.shortcuts import redirect
from dealerfunnel.funnel.library.viewpath import *
from dealerfunnel.funnel.models import *
from dealerfunnel.funnel.library.common import commonfunction 
from dealerfunnel.funnel.library.geocode import *
# Models Plugin Import Here
from dealerfunnel.funnel.model_plugin.base import *
from dealerfunnel.funnel.model_plugin.address import *
from dealerfunnel.funnel.model_plugin.roi_report import *
from dealerfunnel.funnel.model_plugin.customer_model import *
from dealerfunnel.funnel.model_plugin.imageupload import *
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.model.common import common_model
from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo
from django.views.decorators.csrf import csrf_exempt
def loginrequired(func):
   def func_wrapper(slf,request):
       if 'userinfo' in request.session:
           return  func(slf,request) 
       else:
           return HttpResponseRedirect(reverse('login_landing'))
       
   return func_wrapper
class base:
    def __init__(self,request):
        self.request           = request
        self.isdealerlist      = 1
    def setMongo(self):
        client   = MongoClient('localhost:27017')
        return   client.funnel
             
    def redirectloginpage(self):
        url        = reverse('login_landing')
        return HttpResponseRedirect(url)
    def getUserobject(self):
        if 'userinfo' in self.request.session:
            id    = self.request.session['userinfo']['id']
            return User.objects.get(id = id)
        else:
            return None
    def getUserName(self):
        user = self.getUserobject()
        if user is not None:
            return user.name
        else:
            return '' 
    def getusertype(self):
        user  = self.getUserobject()
        return user.type
    def isnotauthentication(self):
        if 'userinfo' in self.request.session:
            return False
        else:
            return True
    def isnotadmin(self):
        return False
        type = self.request.session['userinfo']['type']
        if type == 1:
            return True
        else:
            return False
        
            
    def campaign_setup_session(self):
        if self.menu is not 'CAMPAIGN_SETUP':
            if 'lock1' in self.request.session:
                del self.request.session['lock1']
    def base_management(self,menu):
        self.menu = menu
        self.campaign_setup_session()
    def add_context(self,menu,submenu,context,flag):
        local = context
        menu  = {
                  "base":menu, 
                  "sub":submenu
                }
        dict  = {
                  "local":local,
                  "menu" :menu 
                }
        if flag == 1:
            return Context(dict)
        else:
            return RequestContext(self.request, dict )
    def getdealerlist(self):
        return self.request.session['dealerlist']
    def manageDealer(self):
        user  = self.getUserobject()
        if 'select_id' in self.request.session:
            select_id =  self.request.session['select_id']
            try:
                Dealer.objects.get(id = select_id)
            except ObjectDoesNotExist:
                select_id           = common_model().get_bootstrap_dealer_id()    
        else:
            select_id           = common_model().get_bootstrap_dealer_id()
            self.request.session['select_id'] = select_id
        dealer                   = {}
        if user.usertype ==  1:
            dealer["dealerlist"] = Dealer.objects.all()
        else:
            dealerlist           = self.getdealerlist()
            dealer["dealerlist"] = Dealer.objects.filter(id__in = dealerlist) 
        try:
            dealer["selecteddealer"] = Dealer.objects.get(id = select_id)
        except ObjectDoesNotExist:
            dealer["selecteddealer"] = {}    
        dealer["select_id"]      = select_id
        dealer["isshow"]         = self.isdealerlist
        return dealer
    def template_context(self,menu,submenu,flag):
        userinfo          = self.request.session["userinfo"]
        dealer            = self.manageDealer()
        
        menu              = {
                            "base":menu, 
                            "sub" :submenu
                            }
        dict              = {
                            "menu" :menu,
                            "dealer" : dealer,
                            "userinfo" : userinfo 
                            }
        if flag == 1:
            return Context(dict)
        else:
            return RequestContext(self.request, dict )       
    
    def view_render(self,path,context,menu,submenu,flag=1):
        var               = self.add_context(menu, submenu, context, flag)
        content           = loader.get_template(path).render(var)
        return              HttpResponse( content ) 
    def json_view(self,path,context):
        var               = Context(context)
        return loader.get_template(path).render(var)
    def template_render(self,path,context,menu,submenu,flag=1):
        var               = self.add_context(menu, submenu, context, flag)
        template_var      = self.template_context(menu, submenu,flag)
        meta              = loader.get_template(Path().BASE_META).render(template_var)
        js                = loader.get_template(Path().BASE_JS).render(template_var)
        jsframework       = loader.get_template(Path().BASE_JSFRAMEWORK).render(template_var)
        css               = loader.get_template(Path().BASE_CSS).render(template_var)
        left              = loader.get_template(Path().BASE_LEFT).render(template_var)
        top               = loader.get_template(Path().BASE_TOP).render(template_var)
        jscript           = loader.get_template(Path().BASE_SCRIPTS).render(template_var)
        content           = loader.get_template(path).render(var)  
        return              HttpResponse( meta + css + js + jsframework + top + left +  content + jscript )
    
