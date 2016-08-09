from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.analysis import *
from dealerfunnel.funnel.library.paginator_plugin import *
from dealerfunnel.funnel.model_plugin.customer_model import *
from dealerfunnel.funnel.model_plugin.getcustomer_model import *
from dealerfunnel.funnel.model.customer.getinfo import *
from dealerfunnel.funnel.model.dealer.customeractivity_chart import *
from dealerfunnel.funnel.model.lead.leadsetting import *
from dealerfunnel.funnel.model.note.notes import *
from dealerfunnel.funnel.model.cloudone.lead import *
import csv 
import cStringIO as StringIO
import operator
import datetime
def loginrequired(func):
   def func_wrapper(slf,request):
       if 'userinfo' in request.session:
           return  func(slf,request) 
       else:
           return HttpResponseRedirect(reverse('login_landing'))
       
   return func_wrapper
class setnotes():
    @csrf_exempt
    def postnotes(self,request):
        data                   = {}
        barcode                = int(request.POST['barcode'])
        data['comment']        = request.POST['comment']
        data['agent']          = base(request).getUserName()
        customernotes(barcode).createnote(data)
        return HttpResponse('')
class setappointment():
    def updatecustomer(self,barcode,workphone,homephone,email):
        customer           = Customer.objects.get(id = int(barcode))
        customer.workphone = workphone
        customer.homephone = homephone
        customer.email     = email
        customer.save()
    @csrf_exempt     
    def postapp(self,request):
        barcode          = int(request.POST['app_barcode'])
        if 'app_workphone' in request.POST:
            workphone    = commonfunction().phone_validation(request.POST['app_workphone'])
        else:
            workphone    = ''
        if 'app_homephone' in request.POST:
            homephone    = commonfunction().phone_validation(request.POST['app_homephone'])
        else:
            homephone    = ''    
        if 'app_email' in request.POST:
            email        = request.POST['app_email']
        else:
            email        = ''    
        self.updatecustomer(barcode,workphone,homephone,email)
        appdate      = request.POST['app_date']
        apptime      = request.POST['app_time']
        status       = int(request.POST['app_status'])
        date         = dateformateclass().appdatetime_obj(appdate,apptime)
        data                   = {}
        data['agent']          = base(request).getUserName()
        data['source']         = 'App'
        data['appdatetime']    = date
        data['appstatus']      = status
        leadsetting(barcode,None).setLead(data,1,3) 
        cloaudonelead(barcode).setLead()
        data                   = {}
        if len(request.POST['app_note'].split()) == 0:
           pass
        else:
            data['comment']        = request.POST['app_note']
            data['agent']          = base(request).getUserName()
            customernotes(barcode).createnote(data)
        return HttpResponse('')
class customer():
    def __init__(self):
        self.menu    = 'CUSTOMER'
        self.submenu = ''
    @loginrequired
    def landing(self,request):
        
        # This base function need to call for all url
        base(request).base_management(self.menu)
        return base(request).template_render(Path().CUSTOMER_LANDING,{},self.menu,self.submenu,1)
    @loginrequired
    def dealerpage(self,request):
        
        dealerid = request.GET['dealerid']
        chart = customeractivitychart(dealerid).process()
        analysis         = Customer_analysis.objects.get(fdealer_id = dealerid)
        customer_number  = Customer.objects.filter(fdealer = dealerid).count()
        pagin            = paginator_plugin(customer_number,10,1,1).get()
        customer         = Customer.objects.filter(fdealer = dealerid).order_by('-lastvisit')[pagin['limit']:pagin['offset']]
        #customer         = Customer.objects.filter(fdealer = dealerid).order_by('-lastvisit')
        return base(request).view_render(Path().CUSTOMER_DEALERPAGE,{"chart":chart,"customer":customer,"pagin":customer_number,"analysis":analysis},self.menu,self.submenu,1)
    
    @loginrequired
    def paginfilter(self,request):
        
        dealerid  = request.GET['dealerid']
        cpage     = request.GET['cpage']
        mselected = request.GET['mselected']
        ptype     = request.GET['ptype']
        sortcolum = int(request.GET['sortcolum'])
        sortorder  = int(request.GET['sortorder'])
        columlst  = []
        columlst.append([])
        columlst.append([['fname','-lastvisit','-visit'],['-fname','-lastvisit','-visit']])
        columlst.append([['sales','-lastvisit','-visit'],['-sales','-lastvisit','-visit']])
        columlst.append([['service','-lastvisit','-visit'],['-service','-lastvisit','-visit']])
        columlst.append([['carsold','-lastvisit','-visit'],['-carsold','-lastvisit','-visit']])
        columlst.append([['lastvisit','-visit'],['-lastvisit','-visit']])
        columlst.append([['visit','-lastvisit','-sales','-service'],['-visit','-lastvisit','-sales','-service']])
        columlst.append([['lastvisit','-visit'],['-lastvisit','-visit']])
        sort    = columlst[sortcolum][sortorder]
        sortclass = {"name":"sorting","carsold":"sorting","ro":"sorting","revenue":"sorting","lastactivity":"sorting","visits":"sorting","status":"sorting"}
        sortlist  = ['','name','carsold','ro','revenue','lastactivity','visits','status']
        orderlist = ['sorting_asc','sorting_desc']
        sortclass[sortlist[sortcolum]] = orderlist[sortorder]
        now              = datetime.datetime.now().date()
        if mselected == '2':
            dt            = now - datetime.timedelta(180)
            customer_number  = Customer.objects.filter(fdealer = dealerid).filter(lastvisit__gte = dt).count()
        elif mselected == '3':
            dt1            = now - datetime.timedelta(180)
            dt2            = now - datetime.timedelta(360)
            customer_number  = Customer.objects.filter(fdealer = dealerid).filter(lastvisit__gte = dt2,lastvisit__lt = dt1).count()
        else:
            customer_number  = Customer.objects.filter(fdealer = dealerid).count()    
        pagin            = paginator_plugin(customer_number,20,int(cpage),int(ptype)).get()
        
        pagelst          = range(1,pagin['total_page'] + 1)
        #customer         = Customer.objects.filter(fdealer = dealerid).order_by(*sort)[pagin['limit']:pagin['offset']]
        
        if mselected == '2':
           dt            = now - datetime.timedelta(180) 
           customer      = Customer.objects.filter(fdealer = dealerid).filter(lastvisit__gte = dt).order_by(*sort)[pagin['limit']:pagin['offset']]    
        elif  mselected == '3':
           customer      = Customer.objects.filter(fdealer = dealerid).filter(lastvisit__gte = dt).order_by(*sort)[pagin['limit']:pagin['offset']]       
        else:
           customer      = Customer.objects.filter(fdealer = dealerid).order_by(*sort)[pagin['limit']:pagin['offset']]        
        analysis         = Customer_analysis.objects.get(fdealer_id = dealerid)
        
        
        return base(request).view_render(Path().CUSTOMER_PAGIN,{"analysis":analysis,"dealerid":dealerid,"customer":customer,"pagin":pagin,"sortcolum":sortcolum,"sortorder":sortorder,"sortclass":sortclass,"pagelst":pagelst},self.menu,self.submenu,1)
    
    @loginrequired
    def profile(self,request):
        cid      = request.GET['cid']
        context  = getcustomer(cid,True).dataPopulate()
        context['sales-active']       = ''
        context['service-active']     = '' 
        if context['isSales']:
            context['salesactive']   = 'active'
        else:
            context['serviceactive'] = 'active'    
        baseclass = base(request)
        baseclass.isdealerlist = 0
        return baseclass.template_render(Path().CUSTOMER_PROFILE,context,self.menu,self.submenu,1)
    @loginrequired
    def downloadcsv(self,request):
        # Check Login Authentication
        
        
        def data(dealerid):
            customer    = Customer.objects.filter(fdealer = dealerid).order_by('-lastvisit')
            csvfile = StringIO.StringIO()
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['Fname', 'Lname', 'Address', 'City','State','Zip'])
            yield csvfile.getvalue()
            for n in customer:
                csvfile = StringIO.StringIO()
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([n.fname,n.lname,n.address,n.city,n.state,n.fzip.code])
                yield csvfile.getvalue()

        dealerid = request.GET['dealerid']
        #create the reponse object with a csv mimetype
        response = HttpResponse(
            data(dealerid),
            mimetype='text/csv',
            )
        #Set the response as an attachment with a filename
        dealer  = Dealer.objects.get(id=dealerid)
        name    = dealer.name.replace(" ","_") + '.csv' 
        response['Content-Disposition'] = "attachment; filename=" + name
        response.streaming = True
        return response                   