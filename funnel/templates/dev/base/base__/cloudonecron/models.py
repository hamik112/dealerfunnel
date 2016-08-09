from django.db import models
from django.template.defaultfilters import default
from _mysql import NULL
class State(models.Model):
    state_name           =  models.CharField(max_length=30,null = True)   
    state_abbreviation   =  models.CharField(max_length=30,null = True)
    state_status         =  models.CharField(max_length=30,null = True)
class City(models.Model):
    city                    = models.CharField(max_length=100,null = True)          
class Media_image(models.Model):
    path   = models.TextField(null = True)
    width  = models.IntegerField(null = True)
    height = models.IntegerField(null = True)
    def __dir__(self):
            return [
                      'name','width','height'
                   ]  
class Zipcode(models.Model):
    code    = models.CharField(max_length = 10,null = True)
    lat     = models.FloatField()
    lng     = models.FloatField()
    def __dir__(self):
            return [
                      'code','lat','lng'
                   ]
class Twillio_phone(models.Model):
    number  = models.CharField(max_length = 100,null = True)
    sid     = models.CharField(max_length = 100,null = True)
    date    = models.DateField(null = True)
    type    = models.CharField(max_length = 100, null = True)
    city    = models.CharField(max_length = 100, null = True)
    state   = models.CharField(max_length = 100, null = True)
    zip     = models.CharField(max_length = 100, null = True)
    def __dir__(self):
            return [
                      'number','sid','date','type','city','state','zip'
                   ]
class Dealer(models.Model):
    dealerid                    = models.IntegerField(null= True)
    name                        = models.CharField(max_length=100,null = True)
    address                     = models.CharField(max_length=100,null = True)
    city                        = models.CharField(max_length=50,null = True)
    state                       = models.CharField(max_length=20,null = True)
    fzip                        = models.ForeignKey(Zipcode)
    color                       = models.CharField(max_length=50,null = True)
    flogo                       = models.ForeignKey(Media_image,related_name='image1',null = True)
    fmlogo                      = models.ForeignKey(Media_image,related_name='image2',null = True)
    ftwillio                    = models.ForeignKey(Twillio_phone,related_name='twilio',null = True)
    sale_contact                = models.CharField(max_length = 100,null = True)
    sale_title                  = models.CharField(max_length = 100,null = True)
    sale_phone                  = models.CharField(max_length = 20,null = True)
    service_contact             = models.CharField(max_length = 100,null = True)
    service_title               = models.CharField(max_length = 100,null = True)
    service_phone               = models.CharField(max_length = 20,null = True)
    trade_contact               = models.CharField(max_length = 100,null = True)
    trade_title                 = models.CharField(max_length = 100,null = True)
    trade_phone                 = models.CharField(max_length = 20,null = True)
    sales_regular_hour_from     = models.CharField(max_length = 20,null = True)
    sales_sunday_hour_from      = models.CharField(max_length = 20,null = True)
    sales_saturday_hour_from    = models.CharField(max_length = 20,null = True)
    sales_regular_hour_to       = models.CharField(max_length = 20,null = True)
    sales_sunday_hour_to        = models.CharField(max_length = 20,null = True)
    sales_saturday_hour_to      = models.CharField(max_length = 20,null = True)
    service_regular_hour_from   = models.CharField(max_length = 20,null = True)
    service_sunday_hour_from    = models.CharField(max_length = 20,null = True)
    service_saturday_hour_from  = models.CharField(max_length = 20,null = True)
    service_regular_hour_to     = models.CharField(max_length = 20,null = True)
    service_sunday_hour_to      = models.CharField(max_length = 20,null = True)
    service_saturday_hour_to    = models.CharField(max_length = 20,null = True)
    triggers_budget             = models.IntegerField(null= True)
    triggers_email              = models.IntegerField(null= True)
    triggers_pieces             = models.IntegerField(null = True)
    trigger_cost_per_pieces     = models.FloatField(null = True)
    trigger_trade_cycle         = models.IntegerField(null = True)
    trigger_birthday            = models.IntegerField(null = True)
    trigger_new_purchase        = models.IntegerField(null = True)
    trigger_equity_position     = models.IntegerField(null = True)
    trigger_fst_service         = models.IntegerField(null = True)
    trigger_warranty_expiration = models.IntegerField(null = True)
    trigger_overdue_services    = models.IntegerField(null = True)
    trigger_make_conquest       = models.IntegerField(null = True)
    trigger_crossover_conquest  = models.IntegerField(null = True)
    smsforwardnumber            = models.CharField(max_length = 20,null = True)
    forwardnumber               = models.CharField(max_length = 20,null = True)
    cdate                       = models.DateField(auto_now_add=True)
    keyid                       = models.CharField(max_length=100,null = True)
    flag1                       = models.IntegerField(default=0,null= True)
    flag2                       = models.IntegerField(default=0,null= True)
    flag3                       = models.IntegerField(default=0,null= True)
    flag4                       = models.IntegerField(default=0,null= True)
    outofmarketdistance         = models.IntegerField(default=0,null= True)
    def __dir__(self):
            return [
                    'name','address','city','state','fzip','color','faddress','flogo','fmlogo','ftwillio','sale_contact','sale_title',
                    'sale_phone','service_contact','service_title','service_phone','trade_contact','trade_title',
                    'trade_phone','sales_regular_hour_from','sales_sunday_hour_from','sales_saturday_hour_from',
                    'service_regular_hour_from','service_sunday_hour_from','service_saturday_hour_from',
                    'sales_regular_hour_to','sales_sunday_hour_to','sales_saturday_hour_to',
                    'service_regular_hour_to','service_sunday_hour_to','service_saturday_hour_to',
                    'triggers_budget','triggers_pieces','trigger_cost_per_pieces','trigger_trade_cycle',
                    'trigger_birthday','trigger_new_purchase','trigger_equity_position','trigger_fst_service',
                    'trigger_warranty_expiration','trigger_overdue_services','trigger_make_conquest',
                    'trigger_crossover_conquest','cdate','keyid','triggers_email','smsforwardnumber','forwardnumber','outofmarketdistance'
                    
                   ]
 
class Dealer_cloudone(models.Model):
    fdealer        = models.ForeignKey(Dealer,null = True)
    cmpcloudid     = models.IntegerField(null = True)
    dealercloudid  = models.IntegerField(null = True)
    fd1            = models.CharField(max_length=100,null = True)
    td1            = models.CharField(max_length=100,null = True)
    id1            = models.CharField(max_length=10,null = True)
    fd2            = models.CharField(max_length=100,null = True)
    td2            = models.CharField(max_length=100,null = True)
    id2            = models.CharField(max_length=10,null = True)
    fd3            = models.CharField(max_length=100,null = True)
    td3            = models.CharField(max_length=100,null = True)
    id3            = models.CharField(max_length=10,null = True)
    fd4            = models.CharField(max_length=100,null = True)
    td4            = models.CharField(max_length=100,null = True)
    id4            = models.CharField(max_length=10,null = True)
    fd5            = models.CharField(max_length=100,null = True)
    td5            = models.CharField(max_length=100,null = True)
    id5            = models.CharField(max_length=10,null = True)
    fd6            = models.CharField(max_length=100,null = True)
    td6            = models.CharField(max_length=100,null = True)
    id6            = models.CharField(max_length=10,null = True)
    fd7            = models.CharField(max_length=100,null = True)
    td7            = models.CharField(max_length=100,null = True)
    id7            = models.CharField(max_length=10,null = True)
    cname          = models.CharField(max_length=100,null = True)
    time_zone      = models.CharField(max_length=100,null = True)
    phone          = models.CharField(max_length=100,null = True)
    gender         = models.CharField(max_length=100,null = True)
    pronunciation  = models.CharField(max_length=100,null = True)
    askfor         = models.CharField(max_length=100,null = True)
    notes          = models.CharField(max_length=100,null = True)
    script         = models.CharField(max_length=10,null = True)
    startdate      = models.DateField(null = True)

class usertype_lookup(models.Model):
    user         = models.TextField(max_length=20,null = True)
class User(models.Model):
    name         = models.TextField(max_length=100,null = True)
    title        = models.TextField(max_length=100,null = True)
    email        = models.TextField(max_length=100,null = True)
    password     = models.TextField(max_length=100,null = True)
    fuserphoto   = models.ForeignKey(Media_image,related_name='userphoto',null = True)
    fusertype    = models.ForeignKey(usertype_lookup,related_name='usertype',null = True)
    keyid        = models.TextField(max_length=100,null = True)
    forgottenkey = models.TextField(max_length=100,null = True)
    timedelay    = models.IntegerField(null = True)
    address      = models.TextField(max_length=100,null = True)
    city         = models.TextField(max_length=100,null = True)
    state        = models.TextField(max_length=100,null = True)
    fzip         = models.ForeignKey(Zipcode,null = True) 
    phone        = models.TextField(max_length=100,null = True)
    cellphone    = models.TextField(max_length=100,null = True)
    islogin      = models.IntegerField(null = True,default = 0) 
    lastlogin    = models.DateTimeField(null = True)
    rdate        = models.DateTimeField(null = True)
    status       = models.IntegerField(null = True,default = 1)
    def __dir__(self):
            return [
                      'title','islogin','name','email','password','fuserphoto','fusertype','lastlogin','rdate','keyid','forgottenkey'
                      ,'cellphone','timedelay','address','city','state','fzip','phone','islogin','lastlogin','rdate','status'
                   ]
class User_dealer(models.Model):
    userid        = models.IntegerField(null = True)
    dealerid      = models.IntegerField(null = True)
    def __dir__(self):
            return [
                      'userid','dealerid'
                   ]        
class Lead_address(models.Model):
    fname         = models.CharField(max_length=100,null = True)
    mname         = models.CharField(max_length=100,null = True)
    lname         = models.CharField(max_length=100,null = True)
    address       = models.CharField(max_length=100,null = True)
    city          = models.CharField(max_length=100,null = True)
    state         = models.CharField(max_length=100,null = True)
    zip           = models.CharField(max_length=100,null = True)
class lead(models.Model):
    address       = models.ForeignKey(Lead_address,null = True) 
    consumerid    = models.CharField(max_length=20,null = True)
    dealerid      = models.IntegerField(null= True)
    distance      = models.FloatField(null= True)
    lastvisit     = models.DateField(null= True)
    firstvisit    = models.DateField(null= True)
    dob           = models.DateField(null = True)
    visit         = models.IntegerField(null= True)
    sales         = models.IntegerField(null= True)
    lastsalesdate = models.DateField(null= True)
    service       = models.IntegerField(null= True)
    lastservicedate = models.DateField(null= True)
    istrade       = models.IntegerField(null= True)
    ismarketout   = models.IntegerField(null= True)
    notification  = models.IntegerField(null= True)
    isemail       = models.IntegerField(null= True)
    isdob         = models.IntegerField(null= True)
    isweb         = models.IntegerField(null= True)
    isphone       = models.IntegerField(null= True)
    isapp         = models.IntegerField(null= True)
    phoneduration = models.IntegerField(null= True)
    responseorder = models.IntegerField(null= True)
    islead        = models.IntegerField(null= True) 
    campaignid    = models.IntegerField(null= True)
    label         = models.IntegerField(null= True)
    owner         = models.IntegerField(null= True)
    first_response_date = models.DateTimeField(null = True)
    last_response_date  = models.DateTimeField(null = True)
    couldid       = models.IntegerField(null= True)
    appdate       = models.DateTimeField(null = True)
    appstatus     = models.IntegerField(null= True)    
    notecount     = models.IntegerField(null= True)
    keyid         = models.CharField(max_length = 100,null= True)
class Lead_trade(models.Model):
    lead                 = models.ForeignKey(lead,null = True)
    tid                  = models.CharField(max_length=20,null = True)
    year                 = models.IntegerField(null= True)
    date                 = models.DateField()
class Lead_expiredata(models.Model):
    lead                 = models.ForeignKey(lead,null = True)
    date                 = models.DateField()
    type                 = models.IntegerField(null= True)    
class Zipcode_distance(models.Model):
    zip1    = models.CharField(max_length = 10,null = True)
    zip2    = models.CharField(max_length = 10,null = True)
    val     = models.FloatField()
    def __dir__(self):
            return [
                      'zip1','zip2','val'
                   ]
class Topvehicle(models.Model):
    make              = models.CharField(max_length = 50,null= True)
    model             = models.CharField(max_length = 50,null= True)
    count             = models.IntegerField()
    dealerid          = models.IntegerField(null = True)
class Topzipcode(models.Model):
    zip               = models.CharField(max_length = 10,null= True)
    city              = models.CharField(max_length = 50,null= True)
    state             = models.CharField(max_length = 50,null= True)
    count             = models.IntegerField()
    sales             = models.IntegerField()
    service           = models.IntegerField()
    dealerid          = models.IntegerField(null = True)
class Roi_archive(models.Model):
    date              = models.DateField()
    sales             = models.IntegerField()
    service           = models.IntegerField()
    grossprofit       = models.FloatField()
    roammount         = models.FloatField()
    dealerid          = models.IntegerField(null = True)
class Customer_archive(models.Model):
    date              = models.DateField()
    total             = models.IntegerField()
    active            = models.IntegerField()
    lessactive        = models.IntegerField()
    lost              = models.IntegerField()
    sales             = models.IntegerField(null = True)
    service           = models.IntegerField(null = True)
    both              = models.IntegerField(null = True)
    dealerid          = models.IntegerField(null = True) 
class Customer_analysis(models.Model):
    total_customer     = models.IntegerField(null = True)
    warrantyexpiration = models.IntegerField(null = True)
    crossoverconquest  = models.IntegerField(null = True)
    leaseexpiration    = models.IntegerField(null = True)
    birthday           = models.IntegerField(null = True)
    euityposition      = models.IntegerField(null = True)
    tradecycle         = models.IntegerField(null = True)
    makeconquest       = models.IntegerField(null = True)
    lateservice        = models.IntegerField(null = True)
    active             = models.IntegerField(null = True)
    lessactive         = models.IntegerField(null = True)
    lost               = models.IntegerField(null = True)
    active_12          = models.IntegerField(null = True)
    active_34          = models.IntegerField(null = True)
    active_5           = models.IntegerField(null = True)
    less_12            = models.IntegerField(null = True)
    less_34            = models.IntegerField(null = True)
    less_5             = models.IntegerField(null = True)
    lost_12            = models.IntegerField(null = True)
    lost_34            = models.IntegerField(null = True)
    lost_5             = models.IntegerField(null = True)
    lastvisit          = models.DateField(null = True)
    latestvisit        = models.DateField(null = True)
    bns                = models.IntegerField(null = True)
    snb                = models.IntegerField(null = True)
    bs                 = models.IntegerField(null = True)
    dealerid           = models.IntegerField(null = True)  
class Cron_flag(models.Model):
    status            = models.IntegerField(null = True)
    count             = models.IntegerField(null = True)
    date              = models.DateTimeField(null = True)
         