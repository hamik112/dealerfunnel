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
from dealerfunnel.funnel.model.lead.cloudleadsetting import *
from django.core.exceptions import ObjectDoesNotExist
class cloudoneapi:
    def getFinancial(self,param):
        dic = {}
        
        dic['housingtype'] = ''
        if bool(param['residence_status']):
           dic['housingtype'] = param['residence_status'] 
        
        dic['housingcost'] = ''
        if bool(param['housing_payment']):
           dic['housingcost'] = param['housing_payment']
        
        dic['housinglength'] = ''
        hlength              = 0
        housinglengtht       = ''
        if bool(param['months_at_address']):
           hlength = int(param['months_at_address'])
           if  hlength>0:
               year  = int(hlength/12)  
               month = hlength % 12 
               if year > 0:
                  housinglengtht = str(year) + ' Years'
                  if month > 0:
                    housinglengtht = housinglengtht + ' and ' + str(month) + ' Months'
               else:
                  housinglengtht = str(month) + ' Months'
        dic['housinglength'] = housinglengtht  
        dic['ssn']               = ''    
        if bool(param['ssn']):
           dic['ssn']            = param['ssn'] 
        dic['employer']          = ''
        dic['monthlyincome']     = ''
        dic['years_at_employer'] = ''
        dic['occupation']        = ''   
        if bool(param['jobs']):
            jobs = param['jobs']
            if bool(jobs['job']):
                job = jobs['job'] 
                item = {}
                if type(job) is list:
                   for n in job:
                     item = n
                else:
                    item  = job      
                
                if bool(item['employer']):
                    dic['employer']             = item['employer']
                if bool(item['monthly_income']):
                    dic['monthlyincome']        = item['monthly_income']    
                if bool(item['months_at_employer']):
                    dic['years_at_employer']    = item['months_at_employer']
                if bool(item['occupation']):
                    dic['occupation']           = item['occupation']    
                
        dic['bk']         = ''
        dic['dlnumber']   = ''
        dic['repo']       = ''
        return dic          
               
    def getApp(self,param,agent):
        app  = param['appointment_date']
        part1  = app.split(' ')
        part2  = part1[0].split('-')
        year   = int(part2[0])
        dic    = {}
        dic['isapp'] = 0
        dic['app']   = ''
        if year > 0:
             dic['isapp'] = 1
             data         = {}
             data['agent']          = agent
             data['source']         = 'App'
             data['appdatetime']    = dateformateclass().datetime_obj(app)
             data['appstatus']      = 1
             dic['app']             = data           
        return dic  
    def getCall(self,param):
        calls  = param['calls']
        dic    = {}
        dic['isphone'] = 0
        dic['agent']   = 'Call Center'
        dic['phone']   = {}
        if 'call' in calls:
            dic['isphone'] = 1
            call = calls['call']
            item = []
            if type(call) is list:
                for items in call:
                    data  = {}
                    dic['agent']           = items['agent']
                    data['agent']          = items['agent']
                    data['source']         = 'Call Center'
                    data['duration']       = items['duration']
                    data['direction']      = items['direction']
                    data['recording']      = items['recording']
                    data['disposition']    = items['disposition']
                    appdate                = dateformateclass().datetime_obj(items['date'])
                    data['cloudonetime']   = str(appdate.year) + str(appdate.month) + str(appdate.day) + str(appdate.hour) + str(appdate.minute) + str(appdate.second)
                    data['date']           = appdate
                    item.append(data)
            else:
                data  = {}
                dic['agent']           = call['agent']
                data['agent']          = call['agent']
                data['source']         = 'Call Center'
                data['duration']       = call['duration']
                data['direction']      = call['direction']
                data['recording']      = call['recording']
                data['disposition']    = call['disposition']
                appdate                = dateformateclass().datetime_obj(call['date'])
                data['cloudonetime']   = str(appdate.year) + str(appdate.month) + str(appdate.day) + str(appdate.hour) + str(appdate.minute) + str(appdate.second)
                data['date']           = appdate
                item.append(data)        
            dic['phone'] = item     
        return dic
    def getNotes(self,param):
        notes  = param['notes']
        dic    = {}
        dic['isnote']  = 0
        dic['agent']   = 'Call Center'
        dic['note']    = {}
        if 'note' in notes:
           dic['isnote'] = 1
           note = notes['note']
           item = []
           if type(note) is list:
               for items in note:
                   data  = {}
                   dic['agent']           = items['agent']
                   data['agent']          = items['agent']
                   data['date']           = dateformateclass().datetime_obj(items['date'])
                   data['comment']        = items['note']
                   item.append(data)
           else:
               data  = {}
               dic['agent']           = note['agent']
               data['agent']          = note['agent']
               data['date']           = dateformateclass().datetime_obj(note['date'])
               data['comment']        = note['note']
               item.append(data)
           dic['note'] = item     
        return dic
    @csrf_exempt
    def setcloud(self,request):
        param = json.loads(request.body)
        if type(param['external_id']) is dict:
           return HttpResponse('Invalid Barcode')
        else: 
            barcode            = int(param['external_id'])
            try:
                Customer.objects.get(id = barcode)
                dic   = {}
                dic['barcode'] = barcode
                dic['cloudid'] = param['lead_id']
                call           = self.getCall(param)
                dic['isphone'] = call['isphone']
                dic['phone']   = call['phone']
                note           = self.getNotes(param)
                dic['isnote']  = note['isnote']
                dic['notes']   = note['note']
                if note['isnote'] == 1:
                    agent = note['agent']
                elif dic['isphone'] == 1:
                    agent = call['agent']
                else:
                    agent = 'Call Center'        
                dic['fianancial']    = self.getFinancial(param)
                app            = self.getApp(param,agent)
                dic['isapp']   = app['isapp']
                dic['app']     = app['app']
                message = cloudleadsetting(dic).process()
                return HttpResponse(message)
            except ObjectDoesNotExist:    
                return HttpResponse('Invalid Barcode')
    
    
           
                                   