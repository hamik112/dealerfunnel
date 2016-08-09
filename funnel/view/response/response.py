from dealerfunnel.funnel.view.base import *
from django.core import serializers
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.library.common import *
import json
import pdb
from dealerfunnel.funnel.library.dateformate import *
from django.db.models import Sum
from django.core.paginator import Paginator
from django.db.models import Q
import operator
import time
from django.db import connection
from dealerfunnel.funnel.model_plugin.campaign_model import *
from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from dealerfunnel.funnel.model.lead.leadsetting import *
from dealerfunnel.funnel.model.cloudone.lead import *
class responseapi:
    @csrf_exempt
    def webresponse(self,request):
        param = json.loads(request.body)
        category   = int(param['params']['category'])
        barcode    = param['params']['barcode']
        customer   = Customer.objects.get(id = barcode)
        if category == 1:
            customer.email     = param['params']['email']
            customer.homephone = param['params']['phone']
            customer.save()
        data             = {}
        data['agent']    = ''
        data['source']   = param['params']['source']
        data['trade']    = param['params']['trade']
        data['year']     = param['params']['year']
        data['make']     = param['params']['make']
        data['model']    = param['params']['model']
        data['mileage']  = param['params']['mileage'] 
        label            = param['params']['label']
        leadsetting(barcode,None).setLead(data, label,2)
        cloaudonelead(barcode).setLead()    
        return HttpResponse('Done')
    def lookbarcode(self,request):
        barcode = request.GET['barcode']
        look    = {}
        look['flag'] = 0
        try:
            customer = Customer.objects.get(id = barcode)
            if customer.fcampaign:
                look['flag']    = 1
            else:
                look['flag']    = 2    
            look['fname']   = customer.fname
            look['lname']   = customer.lname
            look['email']   = customer.email
            look['phone']   = customer.homephone
            look['city']    = customer.city
            look['state']   = customer.state
            look['zip']     = customer.zip
            look['address'] = customer.address
            campdic     = {}
            if customer.fcampaign:
                campaign    = Campaign.objects.get(id = customer.fcampaign)
                campdic['campaignname']       = campaign.name
                campdic['dealername']         = customer.fdealer.name
                campdic['dealerid']           = customer.fdealer.id
                campdic['address']            = customer.fdealer.address
                campdic['city']               = customer.fdealer.city
                campdic['state']              = customer.fdealer.state
                campdic['zip']                = customer.fdealer.zip
                campdic['id']                 = customer.fdealer.id
                campdic['twillio']            = commonfunction().phone_formate(customer.fdealer.ftwillio.number,0)
            look['dealer']                    = campdic   
            return HttpResponse(json.dumps(look))
        except ObjectDoesNotExist:
            return HttpResponse(json.dumps(look))
    
    def getyear(self,request):
        year = Makesmodels.objects.values('year').distinct().order_by('-year')
        dic  = []
        dic.append('Please Select')
        for s in year:
            dic.append(s['year'])
        jsondic = {}
        jsondic['year'] = dic
        return HttpResponse(json.dumps(jsondic))
    def getmake(self,request):
        year = request.GET['year']
        make = Makesmodels.objects.filter(year = year).values('make').distinct().order_by('-make')
        dic  = []
        dic.append('Please Select')
        for s in make:
            dic.append(s['make'])
        jsondic = {}
        jsondic['make'] = dic
        return HttpResponse(json.dumps(jsondic))
    def getmodel(self,request):
        year  = request.GET['year']
        make  = request.GET['make']
        model = Makesmodels.objects.filter(year = year).filter(make = make).values('model').distinct().order_by('-model')
        dic  = []
        dic.append('Please Select')
        for s in model:
            dic.append(s['model'])
        jsondic = {}
        jsondic['model'] = dic
        return HttpResponse(json.dumps(jsondic))
    def getdealerlatlng(self,request):
        dealerid = request.GET['id']
        dealer   = Dealer.objects.get(id = dealerid)
        zip          = dealer.zip
        zipcode      = Zipcode.objects.filter(code = zip)[0] 
        dic          = {}
        dic['lat']   = zipcode.lat
        dic['lng']   = zipcode.lng
        dic['code']  = zipcode.code
        return HttpResponse(json.dumps(dic))            
                                   