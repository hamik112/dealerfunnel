from dealerfunnel.funnel.view.base import *
from django.db.models import Q
import operator
import datetime
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.model_plugin.campaign_model import *
import csv 
import cStringIO as StringIO
from dealerfunnel.funnel.library.common import *
class export():
    def __init__(self):
        self.menu    = ''
        self.submenu = ''
    def getLeadList(self,lead,leaddata):
        f = "%Y-%m-%d %H:%M:%S"
        list = []
        list.append(lead['barcode'])
        list.append(lead['lastdate'].strftime(f))
        list.append(leaddata['customer']['fname'])
        list.append(leaddata['customer']['lname'])
        list.append(leaddata['customer']['address'])
        list.append(leaddata['customer']['city'])
        list.append(leaddata['customer']['zip'])
        list.append(leaddata['customer']['email'])
        list.append(leaddata['customer']['homephone'])
        label  = commonfunction().getLabel(lead['label'])
        list.append(label['icone'])
        return list
    
    def export_all_lead(self,request):
        
        def data(filter,res):
            db      = base(res).setMongo()
            csvfile = StringIO.StringIO()
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Barcode','ResponseDate','Fname','Lname','Address','City','State','Zip','Email','Phone','Label'])
            yield csvfile.getvalue()
            alllead = db.lead.find(filter)
            for n in alllead:
                s = db.leaddata.find({"lead":n['_id']})[0]
                csvfile = StringIO.StringIO()
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(self.getLeadList(n,s))
                yield csvfile.getvalue()
        param  = request.session['leadparam']
        
        filter = {}
        filter['dealer']   = param['dealer']
        startDate = dateformateclass().datetime_obj(param['startDate'])
        endDate = dateformateclass().datetime_obj(param['endDate'])
        filter['lastdate'] = { "$gte" :startDate,"$lte":endDate}
        if param['iscampaign']:
            filter['campaign'] = {"$in":param['campaign']}
        if param['istrigger']:
            filter['trigger'] = {"$in":param['trigger']}
        if param['isresponsetype']:
            if param['phoneresponse'] == 1:
               filter['isphone'] = 1
            if param['webresponse'] == 1:
               filter['isweb']  = 1
            if param['appresponse'] == 1:
               filter['isapp']  = 1
                 
        response = HttpResponse(
            data(filter,request),
            content_type='text/csv',
            )
        response['Content-Disposition'] = "attachment; filename=lead.csv"
        response.streaming = True
        return response   
    
    def leadbyid(self,request):
        def data(res):
            idlist  = res.GET['id']
            db      = base(res).setMongo()
            csvfile = StringIO.StringIO()
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Barcode','ResponseDate','Fname','Lname','Address','City','State','Zip','Email','Phone','Label'])
            yield csvfile.getvalue()
            for n in idlist.split(','):
                s = db.leaddata.find({"lead":ObjectId(n)})[0]
                lead = db.lead.find({"_id":ObjectId(n)})[0]
                csvfile = StringIO.StringIO()
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(self.getLeadList(lead,s))
                yield csvfile.getvalue()
             
        
        response = HttpResponse(
            data(request),
            content_type='text/csv',
            )
        #Set the response as an attachment with a filename
        response['Content-Disposition'] = "attachment; filename=lead.csv"
        response.streaming = True
        return response        
                
    def campaign_customer(self,request,cmpkey):
        def data(campaignObj):
            customer    = Customer_campaign.objects.filter(fcampaign = campaignObj)
            csvfile = StringIO.StringIO()
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Pin','Fname', 'Lname', 'Address', 'City','State','Zip'])
            yield csvfile.getvalue()
            for n in customer:
                csvfile = StringIO.StringIO()
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([n.fcustomer.id,n.fcustomer.fname,n.fcustomer.lname,n.fcustomer.address,n.fcustomer.city,n.fcustomer.state,n.fcustomer.zip])
                yield csvfile.getvalue()

        campaignObj = Campaign.objects.get(keyid=cmpkey)
        #create the reponse object with a csv mimetype
        response = HttpResponse(
            data(campaignObj),
            content_type='text/csv',
            )
        #Set the response as an attachment with a filename
        name    = campaignObj.name.replace(" ","_") + '.csv' 
        response['Content-Disposition'] = "attachment; filename=" + name
        response.streaming = True
        return response            
        