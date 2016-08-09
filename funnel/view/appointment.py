from dealerfunnel.funnel.view.base import *
from django.db.models import Q
import operator
import datetime
from dealerfunnel.funnel.library.dateformate import *
from dealerfunnel.funnel.model_plugin.campaign_model import *
from dealerfunnel.funnel.model.campaign.campaigninfo import *
from dealerfunnel.funnel.model.note.notes import *
def loginrequired(func):
   def func_wrapper(slf,request):
       if 'userinfo' in request.session:
           return  func(slf,request) 
       else:
           return HttpResponseRedirect(reverse('login_landing'))
       
   return func_wrapper
class appointment():
    def __init__(self):
        self.menu    = 'CAMPAIGN'
        self.submenu = ''
    def setMongo(self):
        self.client           = MongoClient('localhost:27017')
        self.db               = self.client.funnel
    @loginrequired
    def landing(self,request):
        base(request).base_management(self.menu)
        today     = datetime.datetime.now().date()
        startdate = today - datetime.timedelta(30)
        enddate   = today + datetime.timedelta(30)
        return base(request).template_render('appointment/landing.html',{'startdate':startdate,'enddate':enddate},self.menu,self.submenu,1)
    def activecampaign(self,request):
        dealerid  = int(request.GET['dealerid'])
        activecmp = campaigninfo().getActiveCampaign(dealerid)
        return base(request).view_render('appointment/activecampaign.html',{"cmp":activecmp},self.menu,self.submenu,1)
    def savereschedule(self,request):
        barcode      = int(request.GET['barcode'])
        appstatus    = int(request.GET['app_status'])
        appdate      = request.GET['app_date']
        apptime      = request.GET['app_time']
        date         = dateformateclass().appdatetime_obj(appdate,apptime)
        self.setMongo()
        self.db.lead.update({"barcode":barcode},{"$set":{"appdate":date,"appstatus":appstatus}})
        jsondic      = {}
        jsondic['status']   = base(request).json_view('appointment/appstatus_.html',{"appstatus":appstatus,"barcode":barcode})
        jsondic['datetime'] = base(request).json_view('appointment/timeformate.html',{"date":date})
        jsondic['barcode']  = barcode
        return HttpResponse(json.dumps(jsondic))
    def appstatuschange(self,request):
        barcode   = int(request.GET['barcode'])
        appstatus = int(request.GET['app_status'])
        self.setMongo()
        self.db.lead.update({"barcode":barcode},{"$set":{"appstatus":appstatus}})
        return base(request).view_render('appointment/appstatus.html',{"appstatus":appstatus,"barcode":barcode},self.menu,self.submenu,1)
    def labelchange(self,request):
        barcode   = int(request.GET['barcode'])
        label     = int(request.GET['label'])
        self.setMongo()
        self.db.lead.update({"barcode":barcode},{"$set":{"label":label}})
        return base(request).view_render('appointment/label.html',{"label":label,"barcode":barcode},self.menu,self.submenu,1)
    def ajaxcalenderview(self,request):
        filter  = self.getFilter(request)
        self.setMongo()
        obj   = self.db.lead.find(filter).sort('appdate',pymongo.DESCENDING)
        return base(request).view_render('appointment/ajaxcalenderview.html',{"obj":obj},self.menu,self.submenu,1)
    def addnotes(self,request):
        data                   = {}
        barcode                = int(request.GET['barcode'])
        data['comment']        = request.GET['comment']
        data['agent']          = base(request).getUserName()
        count                  = customernotes(barcode).createnote(data)
        jsondata               = {}
        jsondata['count']      = count
        return HttpResponse(json.dumps(jsondata)) 
    def notemodal(self,request):
        barcode   = int(request.GET['barcode'])
        self.setMongo()
        key  = {"barcode":barcode}
        note = self.db.notes.find(key).sort('date',pymongo.DESCENDING)
        return base(request).view_render('appointment/modal_notes.html',{"notes":note},self.menu,self.submenu,1)
    def getFilter(self,request):
        startdate  = dateformateclass().datetime_obj(request.GET['startdate'] + ' 00:00:00')
        enddate    = dateformateclass().datetime_obj(request.GET['enddate'] + ' 23:59:59')
        cmp        = request.GET['cmpid']
        label      = request.GET['label']
        dealerid   = int(request.GET['dealerid'])
        filter     = {}
        filter['appdate'] = { "$gte" : startdate,"$lte":enddate  }
        filter['isapp']   = 1
        if label!='n':
            filter['label']   = int(label)
        if cmp!='n':
            cmplst = []
            cmplst.append(int(cmp))
            filter['campaign'] = {"$in":cmplst}
        else:
            filter['dealer']   = dealerid
        return filter    
    def reschedulemodal(self,request):
        barcode   = int(request.GET['barcode'])
        self.setMongo()
        app = self.db.lead.find({"barcode":barcode})[0]
        return base(request).view_render('appointment/reschedule.html',{"app":app},self.menu,self.submenu,1)
    def getLead(self,request):
        self.setMongo()
        filter = self.getFilter(request)
        request.session['app_count']  = self.db.lead.find(filter).count()
        pagin = commonfunction().pagination(1,request.session['app_count'],10)
        sortcolumn = int(request.GET['sortcolumn'])
        sortflag   = int(request.GET['sortflag'])
        columlst   = ['fname','campaign_name','appdate','label','appstatus','notecount','lastvisitdate']
        sortlst    = [pymongo.ASCENDING,pymongo.DESCENDING]
        obj   = self.db.lead.find(filter).sort(columlst[sortcolumn],sortlst[sortflag]).skip(0).limit(10)
        dic   = {}
        dic['lead']         = obj
        dic['totalpage']    = pagin['totalpage']
        dic['currentpage']  = 1
        dic['start']        = pagin['start']
        dic['end']          = pagin['end']
        dic['sortcolumn']   = sortcolumn
        dic['sortflag']     = sortflag
        return base(request).view_render('appointment/lead.html',dic,self.menu,self.submenu,1)
    def pagin(self,request):
        self.setMongo()
        filter = self.getFilter(request)
        pagin = commonfunction().pagination(int(request.GET['page']),request.session['app_count'],10)
        obj   = self.db.lead.find(filter).sort('appdate',pymongo.DESCENDING).skip(pagin['offset']).limit(10)
        dic   = {}
        dic['lead']         = obj
        dic['totalpage']    = pagin['totalpage']
        dic['currentpage']  = int(request.GET['page'])
        dic['start']        = pagin['start']
        dic['end']          = pagin['end']
        return base(request).view_render('appointment/lead.html',dic,self.menu,self.submenu,1)
    def getBox(self,request):
        self.setMongo()
        filter = self.getFilter(request)
        lead   = self.db.lead.aggregate([{"$match":filter},{"$group":{"_id":"$appstatus","count":{"$sum":1}}}])
        dic    = {}
        dic['Pending']     = 0
        dic['Rescheduled'] = 0.00
        dic['Reschedule']  = 0
        dic['Show']        = 0
        dic['Noshow']      = 0
        dic['Showrate']    = 0.00
        count              = 0
        for n in lead:
            if n['_id'] == 1:
                dic['Pending']   = dic['Pending'] + int(n['count'])
            if n['_id'] == 2:
                dic['Show']      = dic['Show'] + int(n['count'])
            if n['_id'] == 3:
                dic['Noshow']    = dic['Noshow'] + int(n['count'])
            if n['_id'] == 4:
                dic['Reschedule']= dic['Reschedule'] + int(n['count']) 
        count = dic['Pending'] + dic['Show'] + dic['Noshow'] + dic['Reschedule']
        if dic['Reschedule'] > 0:
            dic['Rescheduled'] = (float(dic['Reschedule']) * 100) / float(count)
        else:
            dic['Rescheduled'] = 0    
        if dic['Show'] > 0:
            dic['Showrate'] = (float(dic['Show']) * 100) / float(count)
        else:
            dic['Showrate'] = 0                            
        
        return base(request).view_render('appointment/box.html',dic,self.menu,self.submenu,1)