from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.library.twilio.rest import TwilioRestClient
from dealerfunnel.funnel.model.customer.getajaxinfo import *
from dealerfunnel.funnel.library.socialphoto import *
class ajax():
    def __init__(self):
        self.menu    = 'Admin'
        self.submenu = 'DEALERSHIP'
    def dealerselect(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        
        request.session['select_id'] = request.GET['select_id']
        return HttpResponse('Hi all')
    def get_app(self,request):
        barcode = int(request.GET['barcode'])
        app     = getcustomerajaxinfo(barcode).getApp()
        return base(request).view_render('ajax/customer_app.html',{"Appointment":app},self.menu,self.submenu,1)
    def get_note(self,request):
        barcode = request.GET['barcode']
        notes     = getcustomerajaxinfo(barcode).getNote()
        return base(request).view_render('ajax/customer_note.html',{"Notes":notes},self.menu,self.submenu,1)
    def get_customer(self,request):
        barcode      = int(request.GET['barcode'])
        customer     = Customer.objects.get(id = barcode)
        return base(request).view_render('ajax/customer_basic.html',{"Basic":customer},self.menu,self.submenu,1)
    def dealermap(self,request):
        barcode      = int(request.GET['barcode'])
        customer     = Customer.objects.get(id = barcode)
        zip          = customer.fdealer.zip
        zipcode      = Zipcode.objects.filter(code = zip)[0]
        return base(request).view_render('ajax/dealermap.html',{"zipcode":zipcode},self.menu,self.submenu,1)
    def get_social_media(self,request):
        barcode      = int(request.GET['barcode'])
        customer     = Customer.objects.get(id = barcode)
        if customer.email:
            photo = socialphoto(customer.email).get()
        else:
            photo = {}
            photo['image']  = '/statics/images/avatar.png'
        return HttpResponse(json.dumps(photo))        