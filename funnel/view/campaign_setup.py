from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.library.paginator_plugin import * 
from django.db.models import Q
from datetime import datetime,timedelta
import pdb
from django.db import connection
import operator
class campaign_setup():
    def __init__(self):
        self.menu         = 'CAMPAIGN_SETUP'
        self.submenu      = ''
    def fieldordermanagement(self,order1,order2,order3,order4,order5):
        orderlist = ['sorting_desc','sorting_asc','sorting']
        list = {}  
        list["order1"] = orderlist[int(order1)]
        list["order2"] = orderlist[int(order2)]
        list["order3"] = orderlist[int(order3)]
        list["order4"] = orderlist[int(order4)]
        list["order5"] = orderlist[int(order5)]  
        return list   
    def getdateobj(self,str):
        return datetime.strptime(str,"%m/%d/%Y").date()
    def updateCustomer(self,lst,cid,enddate):
        for n in lst:
            c = Customer.objects.get(id = n)
            c.fcampaign = cid
            c.notificationcount = c.notificationcount + 1
            c.lastnotification  = enddate
            c.save()
    def updateCustomerCampaign(self,lst,cid):
        for n in lst:
            dic = {}
            dic['fcustomer_id'] = n
            dic['fcampaign_id'] = cid
            dic['customerid'] = n
            dic['campaignid'] = cid
            obj = Customer_campaign(**dic)
            obj.save()
        
    def build_campaign(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        if base(request).isnotadmin():
            return base(request).redirectloginpage()
        tablist = ['','Total Cusomers','Warranty Expiration','Crossover Conquest','Lease Expiration',
                   'Birthday','Equity Position','Trade Cycle','Make Conquest','Late Service'
                  ]
        tab      = int(request.GET['tab'])
        dealerid = int(request.GET['dealerid'])
        name      = tablist[int(request.GET['tab'])]
        mailstyle = request.GET['mailstyle']
        emailstyle = request.GET['emailstyle']
        budgetmonth = request.GET['budgetmonth']
        csdate = self.getdateobj(request.GET['csdate']) 
        cedate = self.getdateobj(request.GET['cedate'])
        mdate = self.getdateobj(request.GET['mdate'])
        emdate = self.getdateobj(request.GET['emdate'])
        budgetmonth = request.GET['budgetmonth']
        cost = request.GET['cost']
        lock   = request.session['lock1']
        dealer = Dealer.objects.get(id = dealerid) 
        dict   = {
                  "name":name,"trigger":tab,"totalmail":lock['total_select'],"totalemail":lock["total_email"],
                  "totalcost":cost,"mailstyle":mailstyle,"emailstyle":emailstyle,"startdate":csdate,
                  "enddate":cedate,"maildate":mdate,"emaildate":emdate,"budgetmonth":budgetmonth,"fdealer":dealer,
                  "type":request.GET['ctype'],"status":request.GET['cstatus']
                 }
        select = lock['select']
        slist  = []
        id = base_model().insert(Campaign(),dict,1)
        keyidh = hashlib.sha224(str(id)).hexdigest()
        Campaign.objects.filter(id = id).update(keyid = keyidh)
        self.updateCustomerCampaign(select,id)
        self.updateCustomer(select,id,cedate)
        
        return HttpResponse('Done')
        
        
        
    @loginrequired    
    def selectcustomer(self,request):
                
        cid   = int(request.GET['cid'])
        val   = int(request.GET['scount'])
        email = int(request.GET['email'])
        tab   = int(request.GET['tab']) 
        lock  = request.session['lock1'] 
        total_select = int(lock["total_select"])
        total_email = int(lock["total_email"])
        select      = lock['select']
        if val == 1:
            select.append(cid)
            total_select = total_select + 1
            total_email  = total_email + email
        else:
            select.remove(cid)
            total_select = total_select - 1
            total_email  = total_email - email
        dict = {"tab":tab,"total_select":total_select,"total_email":total_email,"select":select}
        request.session['lock1'] = dict
        return HttpResponse(request.session['lock1']['total_select'])         
             
    def setsession(self,request,tab):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        if base(request).isnotadmin():
            return base(request).redirectloginpage()
        
        if 'lock1' not in request.session:
            request.session['lock1'] = {"tab":tab,"total_select":0,"total_email":0,"select":[]}
        else:
            dict = request.session['lock1']
            tabs = dict["tab"]
            if tabs != int(tab):
               request.session['lock1'] = {"tab":tab,"total_select":0,"total_email":0,"select":[]}     
        return request.session['lock1']
        
                
                
    def warrantyrangequery(self,wrange,query):
        mylist = []
        today  = datetime.now()
        indexlist = [[0,1000],[0,6],[6,12],[12,18],[18,24],[24,30],[30,36]]     
        if len(wrange) == 1 and wrange[0] == '0':
               return query.filter(customer_roi__warrantyexpiration__gt = today).distinct()
        else:
               for n in wrange:
                   index  = int(n) 
                   start  = today + timedelta(indexlist[index][0]*30)
                   end    = today + timedelta(indexlist[index][1]*30)
                   mylist.append(Q(Q(customer_roi__warrantyexpiration__gte = start) & Q(customer_roi__warrantyexpiration__lte = end)))
        return query.filter(reduce(operator.or_, mylist)).distinct()
    
    def lwarrantyrangequery(self,wrange,query):
        indexlist = [[0,100],[0,6],[6,12],[12,18],[18,24],[24,30],[30,36]]     
        today  = datetime.now()
        mylist = []
        if len(wrange) == 1 and wrange[0] == '0':
            return query.filter(customer_roi__warrantyexpiration__gt = today).distinct()
        else:
            for n in wrange:
                index  = int(n) 
                start  = today + timedelta(indexlist[index][0]*30)
                end    = today + timedelta(indexlist[index][1]*30)
                mylist.append(Q(Q(customer_roi__leaseexpiration__gte = start) & Q(customer_roi__leaseexpiration__lte = end)))
            return query.filter(reduce(operator.or_, mylist)).distinct()
    def tradecyclerange(self,range,year1,year2,query,dealerid):
        indexlist = [[0,100],[0,3],[3,6],[6,12],[0,12],[0,24],[0,36],[0,48],[0,60],[0,72],[0,84],[0,96],[0,108],[0,300]]     
        today  = datetime.now()
        mylist = []
        if len(range) == 1 and range[0] == '0':
            return query.filter(sales__gte = 1)
        else:
            query = Customer_roi.objects.filter(fdealer = 7).filter(type = 1).filter(istradein = 0)
            mylist = []
            for n in range:
                index  = int(n) 
                start  = today - timedelta(indexlist[index][0]*30)
                end    = today - timedelta(indexlist[index][1]*30)
                mylist.append(Q(Q(entrydate__gte = end) & Q(entrydate__lte = start)))
            query =  query.filter(reduce(operator.or_, mylist))
            if year1 !='' and year2 !='':
               y1 = int(year1)
               y2 = int(year2)
       
               if y1 < y2:
                  yy1 = y1
                  yy2 = y2 + 1
               else:
                  yy1 = y2
                  yy2 = y1 + 1 
               mylist = []
               while (yy1 < yy2):
                  mylist.append(Q(year = yy1))
                  yy1 = yy1 + 1
               query = query.filter(reduce(operator.or_, mylist)).distinct()   
            c = query.values_list('fcustomer', flat=True).distinct()
            return Customer.objects.filter(id__in = c)
        
    def birthdayquery(self,month,query):
        mylist = []
        if int(month[0]) == 0:
            return  query.filter(isbirthday = 1)
        else:
            for n in month:
                mn = int(n)
                mylist.append(Q(birth_date__month = mn))
        return query.filter(reduce(operator.or_, mylist))        
    
    def tabfilterview(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        if base(request).isnotadmin():
            return base(request).redirectloginpage()
        
        dealerid = int(request.GET['dealerid'])
        topnav   = int(request.GET['topnav'])
        query    = Customer.objects.filter(fdealer = dealerid)
        lock     = self.setsession(request,topnav)
        fieldid  = 2
        ordestatus  = 1
        #pdb.set_trace()
        select   = lock["select"]
        if topnav == 2:
            query = self.warrantyrangequery(["0"],query)
        if topnav == 4:
            query = self.lwarrantyrangequery(["0"],query)
        if topnav == 7:
            query = query.filter(sales__gte = 1).distinct()
        if topnav == 5:
            query = query.filter(birth_date__gte = '1900-01-01')
        if topnav == 9:
            query = query.filter(customer_roi__service_delay__gte = 180).distinct()
        number   = query.count()
        pagin    = paginator_plugin(number,100,1,1).get()
        customer = query.order_by('-lastvisit')[pagin['limit']:pagin['offset']]       
        
        pagenumber = []
        i =1
        for n in range(pagin['total_page']):
            pagenumber.append(i)
            i = i + 1
        resultdict             = {}
        resultdict["session"] = lock
        resultdict["customer"] = customer
        resultdict["pagin"]    = pagin
        resultdict["pagenumber"]    = pagenumber
        resultdict["total_customer"]    = number
        resultdict["selected_count"]    = lock["total_select"]
        resultdict["dealerid"] = dealerid
        resultdict['selected_email'] = lock["total_email"]
        dealerinfo   = Dealer.objects.get(id=dealerid)
        resultdict['cost_per_pieces'] = dealerinfo.trigger_cost_per_pieces
        #resultdict["cost"]    = resultdict['cost_per_pieces'] * lock["total_select"]
        resultdict["cost"]    = 0

        for n in customer:
            if n.id in select:
                n.select = 1
            else:
                n.select = 0
                
        resultdict["customer"] = customer
        resultdict["orderstatus1"] = 1
        resultdict["orderstatus2"] = 2
        resultdict["orderstatus3"] = 2
        resultdict["orderstatus4"] = 2
        resultdict["orderstatus5"] = 2    
        resultdict["order"] = self.fieldordermanagement(1,2,2,2,2)
        resultdict["query"] = connection.queries 
        return base(request).view_render(Path().CAMPAIGN_SETUP_TABVIEW,resultdict,self.menu,self.submenu,1)
        
        
    def filterQuery(self,dealerid,topnav,distance,ncount,isdate,sdate,edate,
                    isnt,sndate,endate,cpage,ptype,customertype,iswarranty,warrantyrange,
                    islwarranty,lwarrantyrange,isbirthday,birthdaymonth,isndate,searchitem,issearch,
                    vyear1,vyear2,tradeinrange
                    ):
        query             = Customer.objects.filter(fdealer = dealerid)
        if topnav == 2:
            if iswarranty == 0:
                query = query.filter(iswarrantyexpiration = 1)
            else:
                query = self.warrantyrangequery(warrantyrange,query)     
                    
        if topnav == 4:
            if islwarranty == 0:
                query = query.filter(isleaseexpiration = 1)
            else:
                query = self.lwarrantyrangequery(lwarrantyrange,query)    
        if topnav == 5:
            if isbirthday == 0:
                query = query.filter(birth_date__gte = '1900-01-01')
            else:
                query = self.birthdayquery(birthdaymonth,query)    
                    
        if topnav == 7:
            query = self.tradecyclerange(tradeinrange,vyear1,vyear2,query,dealerid)
            
        if topnav == 9:
            query = query.filter(customer_roi__service_delay__gte = 180).distinct()
        if isndate == 1:
            query = query.filter(lastnotification__gte = sndate,lastnotification__lte = endate)
        if isdate == 1:
            query = query.filter(lastvisit__gte = sdate,lastvisit__lte = edate)
        dislist   = [[-100.00,5000000.00],[0.00,5.00],[5.00,10.00],[10.00,15.00],[15.00,20.00],[20.00,50000.00]]
       
        
        mylist = []
        for n in distance:
            mylist.append(Q(Q(distance__gte = dislist[int(n)][0]) & Q(distance__lte = dislist[int(n)][1])))
        query = query.filter(reduce(operator.or_, mylist))
        if isnt == 1:
            mylist = []
            for n in ncount:
                mylist.append(Q(notificationcount = int(n)))
            query = query.filter(reduce(operator.or_, mylist))    
        
        mylist = []
        activedate = datetime.now() - timedelta(180)
        lessactive = datetime.now() - timedelta(365)
        if int(customertype[0]) > 0:
            for n in customertype:
                if n == '1':
                    mylist.append(Q(lastvisit__gte = activedate))
                if n == '2':
                    mylist.append(Q(lastvisit__gte = lessactive,lastvisit__lt = activedate))
                if n == '3':
                    mylist.append(Q(lastvisit__lt = lessactive))    
            query = query.filter(reduce(operator.or_, mylist))
        if issearch == 1:
           mylist = []
           n = searchitem.split(' ')
           for s in n:
               mylist.append(Q(fname__icontains = s))
               mylist.append(Q(lname__icontains = s))
               mylist.append(Q(homephone__icontains = s))
               mylist.append(Q(pin__icontains = s))
               mylist.append(Q(city__icontains = s))
           query = query.filter(reduce(operator.or_, mylist))   
        return query
    def orderquery(self,query,order1,order2,order3,order4,order5):
        orderlist      = []
        if order1 == 1:
            orderlist.append('-lastvisit')
        if order1 == 0:
            orderlist.append('lastvisit')    
        if order2 == 1:
            orderlist.append('-distance')
        if order2 == 0:
            orderlist.append('distance')
        if order3 == 1:
            orderlist.append('-status')
        if order3 == 0:
            orderlist.append('status')
        if order4 == 1:
            orderlist.append('-city')
        if order4 == 0:
            orderlist.append('city')
        if order5 == 1:
            orderlist.append('-fname')
        if order5 == 0:
            orderlist.append('-fname')
        return query.order_by(*orderlist)
                        
    def filterCustomer(self,dealerid,topnav,distance,ncount,isdate,sdate,edate,isnt,
                       sndate,endate,cpage,ptype,customertype,iswarranty,warrantyrange,
                       islwarranty,lwarrantyrange,isbirthday,birthdaymonth,isndate,searchitem,issearch,
                       orderstatus1,orderstatus2,orderstatus3,orderstatus4,orderstatus5,vyear1,vyear2,tradeinrange
                       ):
        query    = self.filterQuery(dealerid, topnav, distance, ncount, isdate, sdate, edate, isnt, 
                       sndate, endate, cpage, ptype, customertype,iswarranty,warrantyrange,
                       islwarranty,lwarrantyrange,isbirthday,birthdaymonth,isndate,searchitem,issearch,vyear1,vyear2,tradeinrange
                       )
        number   = query.count()
        pagin    = paginator_plugin(number,100,cpage,ptype).get()
        
        query  = self.orderquery(query,orderstatus1,orderstatus2,orderstatus3,orderstatus4,orderstatus5)
        customer = query[pagin['limit']:pagin['offset']]  
        ordera    = self.fieldordermanagement(orderstatus1,orderstatus2,orderstatus3,orderstatus4,orderstatus5)
        lista     = {"pagin":pagin,"customer":customer,"number":number,"query":connection.queries,"order":ordera}  
        
        return lista                   
            
    def paginsearch(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        if base(request).isnotadmin():
            return base(request).redirectloginpage()
        
        cpage             = request.GET['cpage']
        ptype             = request.GET['ptype']
        dealerid          = request.GET['dealerid']
        customer_number   = Customer.objects.all().filter(fdealer = dealerid).count()
        pagin             = paginator_plugin(customer_number,10,cpage,ptype).get()
        enddate           = datetime.datetime.now()
        customer          = Customer.objects.filter(fdealer = dealerid).order_by('-lastvisit')[pagin['limit']:pagin['offset']]  
        return base(request).view_render(Path().CAMPAIGN_SETUP_SPAGIN,{"customer":customer,"pagin":pagin},self.menu,self.submenu,1)
    def searchresult(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        if base(request).isnotadmin():
            return base(request).redirectloginpage()
        
        lock   = request.session['lock1']
        selectcustomer = lock["select"]
        dealerid  = int(request.GET['dealerid'])
        customer_list     = self.filterCustomer(int(request.GET['dealerid']),int(request.GET['topnav']),request.GET['distance'].split(","),request.GET['notification'].split(","),
                                               int(request.GET['isdate']),request.GET['sdate'],request.GET['edate'],int(request.GET['isnotification']),
                                               request.GET['sndate'],request.GET['endate'],request.GET['cpage'],request.GET['ptype'],request.GET['customertype'].split(","),
                                               int(request.GET['iswarrantyrange']),request.GET['warrantyrange'].split(","),int(request.GET['islwarrantyrange']),request.GET['lwarrantyrange'].split(","),
                                               int(request.GET['isbirthday']),request.GET['birthdaymonth'].split(","),int(request.GET['isndate']),request.GET['searchitem'],int(request.GET['issearch']),
                                               int(request.GET['orderstatus1']),int(request.GET['orderstatus2']),int(request.GET['orderstatus3']),int(request.GET['orderstatus4']),int(request.GET['orderstatus5']),
                                               request.GET['vyear1'],request.GET['vyear2'],request.GET['tradeinrange'].split(",")
                                               )
        pagin = customer_list["pagin"]
        pagenumber = []
        i =1
        for n in range(pagin['total_page']):
            pagenumber.append(i)
            i = i + 1
        resultdict             = {}
        resultdict["customer"] = customer_list["customer"]
        resultdict["pagin"]    = customer_list["pagin"]
        resultdict["pagenumber"]    = pagenumber
        resultdict["order"]    = customer_list["order"]
        resultdict["total_customer"]    = customer_list["number"]
        resultdict["query"]    = customer_list["query"]
        resultdict["selected_count"]    = lock['total_select']
        resultdict["dealerid"] = int(request.GET['dealerid'])
        resultdict['selected_email'] = lock['total_email']
        dealerinfo   = Dealer.objects.get(id=dealerid)
        resultdict['cost_per_pieces'] = dealerinfo.trigger_cost_per_pieces
        resultdict["cost"]    = resultdict['cost_per_pieces'] * resultdict["selected_count"]
        resultdict["orderstatus1"]    = int(request.GET['orderstatus1'])
        resultdict["orderstatus2"]    = int(request.GET['orderstatus2'])
        resultdict["orderstatus3"]    = int(request.GET['orderstatus3'])
        resultdict["orderstatus4"]    = int(request.GET['orderstatus4'])
        resultdict["orderstatus5"]    = int(request.GET['orderstatus5'])
        resultdict["searchitem"]    = request.GET['searchitem']
        customer  = resultdict["customer"]
        for n in customer:
            if n.id in selectcustomer:
                n.select = 1
            else:
                n.select = 0
        resultdict["customer"] = customer            
        return base(request).view_render(Path().CAMPAIGN_SETUP_SEARCHF,resultdict,self.menu,self.submenu,1)
    def select_range(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        if base(request).isnotadmin():
            return base(request).redirectloginpage()
        
        query  = self.filterQuery(int(request.GET['dealerid']),int(request.GET['topnav']),request.GET['distance'].split(","),request.GET['notification'].split(","),
                                               int(request.GET['isdate']),request.GET['sdate'],request.GET['edate'],int(request.GET['isnotification']),
                                               request.GET['sndate'],request.GET['endate'],request.GET['cpage'],request.GET['ptype'],request.GET['customertype'].split(","),
                                               int(request.GET['iswarrantyrange']),request.GET['warrantyrange'].split(","),int(request.GET['islwarrantyrange']),request.GET['lwarrantyrange'].split(","),
                                               int(request.GET['isbirthday']),request.GET['birthdaymonth'].split(","),int(request.GET['isndate']),request.GET['searchitem'],int(request.GET['issearch']),
                                               request.GET['vyear1'],request.GET['vyear2'],request.GET['tradeinrange'].split(","))
        
        dealerinfo   = Dealer.objects.get(id=int(request.GET['dealerid'])) 
        cost_per_pieces = dealerinfo.trigger_cost_per_pieces
        selecttype = int(request.GET['selecttype'])
        if selecttype == 2:
           dict      = request.session['lock1']
           ndict     = {}
           ndict["tab"] = dict["tab"]
           ndict["total_select"] = 0
           ndict["total_email"] = 0
           ndict["select"] = [] 
           request.session['lock1'] = ndict 
        else:
            if selecttype == 3:
                sr       = int(request.GET['srange'])
                if sr>0:
                    sr = sr - 1
                er       = int(request.GET['erange'])
                query  = self.orderquery(query,int(request.GET['orderstatus1']),int(request.GET['orderstatus2']),int(request.GET['orderstatus3']),int(request.GET['orderstatus4']),int(request.GET['orderstatus5'])) 
                query = query[sr:er] 
            list1 = []
            for n in query:
                list1.append(int(n.id))
            myset     = list(set(list1))
            number    = len(myset)
            email     = Customer.objects.filter(id__in=myset).filter(email__isnull=False).count()
            dict      = request.session['lock1']
            ndict     = {}
            ndict["tab"] = dict["tab"]
            ndict["total_select"] = number
            ndict["total_email"] = email
            ndict["select"] = myset 
            request.session['lock1'] = ndict
            
                
        
        return self.searchresult(request)     
    def toggleselection(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        if base(request).isnotadmin():
            return base(request).redirectloginpage()
        
        query  = self.filterQuery(int(request.GET['dealerid']),int(request.GET['topnav']),request.GET['distance'].split(","),request.GET['notification'].split(","),
                                               int(request.GET['isdate']),request.GET['sdate'],request.GET['edate'],int(request.GET['isnotification']),
                                               request.GET['sndate'],request.GET['endate'],request.GET['cpage'],request.GET['ptype'],request.GET['customertype'].split(","),
                                               int(request.GET['iswarrantyrange']),request.GET['warrantyrange'].split(","),int(request.GET['islwarrantyrange']),request.GET['lwarrantyrange'].split(","),
                                               int(request.GET['isbirthday']),request.GET['birthdaymonth'].split(","),int(request.GET['isndate']),request.GET['searchitem'],int(request.GET['issearch']),
                                               request.GET['vyear1'],request.GET['vyear2'],request.GET['tradeinrange'].split(","))
        
        dealerinfo      = Dealer.objects.get(id=int(request.GET['dealerid'])) 
        cost_per_pieces = dealerinfo.trigger_cost_per_pieces
        customersession = request.session['lock1']
        scustomer       = customersession['select']
        ndict     = {}
        ndict["tab"] = customersession["tab"]
        
        query  = self.orderquery(query,int(request.GET['orderstatus1']),int(request.GET['orderstatus2']),int(request.GET['orderstatus3']),int(request.GET['orderstatus4']),int(request.GET['orderstatus5']))
        mylist   = []
        i = 0
        for n in query:
            if int(n.id) not in scustomer:
                mylist.append(int(n.id))
                i = i + 1
        
        ndict["total_select"] = i
        ndict["total_email"] = Customer.objects.filter(id__in=mylist).filter(isemail=1).count()
        ndict["select"] = mylist 
        request.session['lock1'] = ndict
        return self.searchresult(request)    
    def getanalysis(self,dealerid):
        dict = {}
        today  = datetime.now()
        dict["total_customer"] = Customer.objects.filter(fdealer = dealerid).count()
        dict["warrantyexpiration"] = Customer.objects.filter(fdealer = dealerid).filter(customer_roi__warrantyexpiration__gt = today).distinct().count()
        dict["leaseexpiration"] = Customer.objects.filter(fdealer = dealerid).filter(customer_roi__leaseexpiration__gt = today).distinct().count()
        dict["birthday"] = Customer.objects.filter(fdealer = dealerid).filter(birth_date__gte = '1900-01-01').count()
        dict["euityposition"] = 0
        dict["crossoverconquest"] = 0
        sdate = datetime.now() - timedelta(180)
        dict["tradecycle"] = Customer.objects.filter(fdealer = dealerid).filter(tradecycle = 1).count()
        dict["makeconquest"] = 0
        dict["lateservice"] = Customer.objects.filter(fdealer = dealerid).filter(last_service_date__lt = sdate).count()
        return dict
    def landing(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        if base(request).isnotadmin():
            return base(request).redirectloginpage()
        
        dealer            = {}
        key               = Dealer.objects.get(keyid = request.GET['id'])
        dealerid          = key.id
        dealer["dealerlist"]     = Dealer.objects.all()
        dealer["selecteddealer"] = Dealer.objects.get(id = dealerid)
        userinfo          = request.session["userinfo"]
        c                 = customer_model(dealerid,'','')
        analysis          = self.getanalysis(dealerid)
        diff              = 1200
        redirect          = Path().Domain + 'dealership/setup/campaign/?id=' + key.keyid
        return base(request).view_render(Path().CAMPAIGN_SETUP_LANDING,{"domain":Path().Domain,"dealer":dealer,"analysis":analysis,"dealerid":key.id,"diff":diff,"key":redirect,"userinfo":userinfo},self.menu,self.submenu,1)
               