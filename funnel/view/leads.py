from dealerfunnel.funnel.view.base import *
def loginrequired(func):
   def func_wrapper(slf,request):
       if 'userinfo' in request.session:
           return  func(slf,request) 
       else:
           return HttpResponseRedirect(reverse('login_landing'))
       
   return func_wrapper
class leads():
    def __init__(self):
        self.menu    = 'CUSTOMER'
        self.submenu = ''
    
    def template_render(self,context,request):
        var           = {}
        var['dealerlist'] = base(request).manageDealer()
        var['userinfo']   = request.session["userinfo"]
        top               = loader.get_template('leads/top.html').render(Context(var))  
        landing           = loader.get_template('leads/landing.html').render(Context(context))
        bottom            = loader.get_template('leads/bottom.html').render(Context({}))
        return              HttpResponse( top + landing + bottom )
    @loginrequired
    def landing(self,request):
        end_date     = datetime.datetime.now().date()
        start_date   = end_date - datetime.timedelta(29)
        user         = User.objects.all()
        dealerlist   = base(request).manageDealer()
        return self.template_render({"user":user,"start":start_date,"end":end_date,"dealer":dealerlist['selecteddealer']}, request)