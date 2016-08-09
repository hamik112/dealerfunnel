from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.library.twilio.rest import TwilioRestClient
from dealerfunnel.funnel.library.mail import dealerfunnelmail
from django.template.loader import get_template
from django.core.mail import EmailMessage
import sys
from django.views.decorators.csrf import csrf_exempt
import pdb
import random
from dealerfunnel.funnel.model_plugin.response_setting_model import *
from dealerfunnel.funnel.model_plugin.response_setting_mongo import *
from dealerfunnel.funnel.model.lead.leadsetting import *
import datetime

class randomlead:
    def selectpin(self,campaignObj):
        customer = Customer_campaign.objects.filter(fcampaign = campaignObj)
        clen      = len(customer) - 1
        index    = random.randint(0,clen)
        self.selected_customer = customer[index].fcustomer
        self.pin  = self.selected_customer.id
        self.dealerObj = self.selected_customer.fdealer
    def setResponseType(self):
        tp   = 2
        return tp
    def setLabelType(self):
        tp   = random.randint(1,6)
        return tp
    def setDate(self):
        year  = str(2016)
        day  = str(random.randint(1,24))
        month = str(random.randint(3,4))
        hour  = str(random.randint(1,23))
        min   = str(random.randint(0,59))
        sec   = str(30)
        self.datetime = year+'-'+month+'-'+day+' '+hour + ':'+min+':'+sec 
        self.datetime = dateformateclass().datetime_obj(self.datetime)
        now   = datetime.datetime.now()
        if self.datetime > now:
           self.datetime = now 
    def setAppDate(self):
        year  = str(2016)
        day   = str(random.randint(1,30))
        month = str(4)
        hour  = str(0)
        min   = str(0)
        sec   = str(0)
        self.datetime = year+'-'+month+'-'+day+' '+hour + ':'+min+':'+sec 
        self.datetime = dateformateclass().datetime_obj(self.datetime)
        return self.datetime
    def phonenumber(self):
        pstr = '0'
        for n in range(0,9):
            pstr = pstr + str(random.randint(0,n))
        return pstr
    
    def setlead(self,request):
        id = request.GET['id']
        count = int(request.GET['count'])
        for n in range(0,count):
            self.setrandomlead(id)
        return  HttpResponse('Lead Created')      
    def set_phonecall(self):
        data  = {}
        data['sid']                 = 'FTRE456F66H'
        data['tophone']             = self.phonenumber()
        data['fromphone']           = self.phonenumber()
        data['callduration']        = random.randint(1,100)
        data['callstatus']          = 'Inbound'
        data['recordingduration']   = random.randint(1,100)
        data['recordingurl']        = 'url.mp3'
        data['calltype']            = 1
        return data
    def setfinancialinfo(self):
        info   = {}
        info['birth_month']            = ''
        info['birth_day']              = ''
        info['birth_year']             = ''
        info['years_at_employer']      = ''
        info['ssn']                    = ''
        info['employer']               = ''
        info['occupation']             = ''
        info['timeemployed']           = ''
        info['monthlyincome']          = ''
        info['housingtype']            = ''
        info['housingcost']            = ''
        info['housinglength']          = ''
        info['bk']                     = ''
        info['repo']                   = ''
        info['dlnumber']               = ''
        return info
    def setrandomlead(self,id):
        response = {}
        response['customerObj']     = self.selected_customer
        response['labelObj']        = self.setLabelType()
        response['responsetypeObj'] = self.setResponseType()
        response['sourceObj']       = 'verifyPrize.com'
        response['call']            = self.set_phonecall()
        response['agent']           = 'agent'
        response['date']            = self.datetime
        response['app']             = {}
        response['financialinfo']   = self.setfinancialinfo()
        response_setting_mongo(response).setResponse()
    def getWebresponse(self):
        data  = {}
        data['agent'] = 'Khalid'
        data['source'] = 'verifyPrize.com'
        return data
    def getPhoneresponse(self):
        data  = {}
        data['agent']          = 'Khalid'
        data['source']         = 'verifyPrize.com'
        data['duration']       =  20
        data['direction']      = 'Inbound'
        data['recording']      = 'http://kolber.github.io/audiojs/demos/mp3/juicy.mp3'
        data['disposition']    = 'disposition'
        data['cloudonetime']   = '19202002'
        return data
    def getAppresponse(self):
        data                   = {}
        data['agent']          = 'Khalid'
        data['source']         = 'App'
        data['appdatetime']    = self.setAppDate()
        data['appstatus']      = 1
        return data
def leadset(request):
        count = 100
        id    = 3
        campaignobj = Campaign.objects.get(id = id)
        for n in range(0,count):
            rnd = randomlead()
            rnd.selectpin(campaignobj)
            response = rnd.getAppresponse()
            label    = random.randint(1,6)
            rnd.setDate()
            leadsetting(rnd.pin,rnd.datetime).setLead(response,label,3)
                