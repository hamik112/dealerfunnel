from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.analysis import *
from dealerfunnel.funnel.library.paginator_plugin import * 
from dealerfunnel.funnel.library.common import *
from dealerfunnel.funnel.model_plugin.response_setting_model import *
import csv
import datetime
from django.views.decorators.csrf import csrf_exempt
import pdb
class responseapi():
    def __init__(self):
        self.menu    = ''
        self.submenu = ''
    
    
    @csrf_exempt
    def setresponse(self,request):
        response = {}
        response['barcode']         = request.POST['barcode']
        response['customer']        = self.setcustomer(request)
        response['financialinfo']   = self.set_financial_info(request)
        response['desiredvehicle']  = self.set_desired_vehicle(request)
        response['trade']           = self.set_trade(request)
        response['customerObj']     = Customer.objects.get(id = request.POST['customerid'])
        response['dealerObj']       = Dealer.objects.get(id = request.POST['dealerid'])
        response['labelObj']        = self.getResponseLabelIdbyTag(request.POST['label'])
        response['responsetypeObj'] = self.getResponseTypeIdbyTag(request.POST['responsetype'])
        response['sourceObj']       = self.getSource(request.POST['source'])
        response['campaignObj']     = Campaign.objects.get(id = response['customerObj'].fcampaign)
        response['buytimeObj']      = self.getBuytime(request.POST['buytime'])
        response_setting(response).setResponse()
        return  HttpResponse('Lead Created')  
    def getBuytime(self,time):
        if time == '':
            return Customer_buytime.objects.get(flag = 0)
        else:
            if Customer_buytime.objects.filter(tag=time).exists():
                return Customer_buytime.objects.get(tag=time)
            else:
                dir = {}
                dir['flag'] = 1
                dir['tag']  = time
                return base_model().insert(Customer_buytime(),dir,2)
    def getSource(self,source):
        sourceObj = Response_source.objects.filter(source = source)
        if len(sourceObj) == 0:
            dict                         = {"source":source}
            return base_model().insert(Response_source(),dict,2)
        else:
            return Response_source.objects.get(source = source)
        
    def getResponseTypeIdbyTag(self,tag):
        typeObj = Response_type.objects.get(type = tag)
        return typeObj
    def getResponseLabelIdbyTag(self,tag):
        labelObj = Response_label.objects.get(label = tag)
        return labelObj    
    def set_trade(self,request):
        data  = {}
        data['year']         = request.POST['year']
        data['make']         = request.POST['make']
        data['model']        = request.POST['model']
        data['mileage']      = commonfunction().removecomma(request.POST['mileage'])
        data['book_value']   = commonfunction().removecomma(request.POST['book_value'])
        data['payment']      = commonfunction().removecomma(request.POST['payment'])
        data['payoff']       = commonfunction().removecomma(request.POST['payoff'])
        data['apr']          = request.POST['apr']
        return data    
    def set_desired_vehicle(self,request):
        data  = {}
        data['type']        = request.POST['type']
        data['style']       = request.POST['style']
        data['specific']    = request.POST['specific']
        data['downpayment'] = request.POST['downpayment']
        return data    
    def set_financial_info(self,request):
        data  = {}
        data['dob']           = dateformateclass().getdate_obj(request.POST['dyear'],request.POST['dmonth'],request.POST['dday'])
        data['ssn']           = commonfunction().phone_validation(request.POST['ssn'])
        data['employer']      = request.POST['employer']
        data['occupation']    = request.POST['occupation']
        data['timeemployed']  = request.POST['timeemployed']
        data['monthlyincome'] = commonfunction().removecomma(request.POST['monthlyincome'])
        data['housingtype']   = request.POST['housingtype']
        data['housingcost']   = commonfunction().removecomma(request.POST['housingcost'])
        data['bk']            = request.POST['bk']
        data['repo']          = request.POST['repo']
        data['dlnumber']      = request.POST['dlnumber']
        return data        
    def setcustomer(self,request):
        data     = {}
        data['fname'] = request.POST['fname']
        data['lname'] = request.POST['lname']
        data['email'] = request.POST['email']
        data['address'] = request.POST['address']
        data['city'] = request.POST['city']
        data['state'] = request.POST['state']
        data['zip'] = request.POST['zip']
        data['date'] = request.POST['date']
        data['homephone'] = commonfunction().phone_validation(request.POST['phone'])
        return data 
            