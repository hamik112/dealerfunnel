from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.campaign_model import *
import json
import datetime
class login():
    def __init__(self):
        self.menu    = 'login'
        self.submenu = ''
    def landing(self,request):
        return base(request).view_render(Path().LOGINLANDING,{},self.menu,self.submenu,2)
    def forgotpassword(self,request):
        return base(request).view_render(Path().FORGOTPASSWORD,{},self.menu,self.submenu,1)
    def changepasswordupdate(self,request):
        keyid = request.POST['userid']
        password = request.POST['password']
        count     = User.objects.filter(forgottenkey = keyid).count()
        if count == 1:
            user =  User.objects.get(forgottenkey = keyid)
            user.password = password
            user.forgottenkey = ''
            user.save()
        url        = reverse('login_landing')
        return HttpResponseRedirect(url)        
    def changepassword(self,request,keyid):
        id    = keyid
        dict  = {"flag":1}
        if id == '':
            dict["flag"] = 0
        else:    
            count = User.objects.filter(forgottenkey = id).count()
            if count == 1:
                dict["id"] = keyid
            else:
                dict["flag"] = 0    
        return base(request).view_render(Path().CHANGEPASSWORD,{"info":dict},self.menu,self.submenu,2)         
    def jsoncheck(self,request):
        username  = request.GET['username']
        password  = request.GET['password']
        user      = User.objects.filter(email = username).filter(password = password).count()
        dict      = {"islogin":user}
        return HttpResponse(json.dumps(dict), content_type="application/json")
    def submit(self,request):
        username               = request.POST['username']
        password               = request.POST['password']
        user                   = User.objects.filter(email = username).filter(password = password)
        dict                   = {}
        for n in user:
            dict["id"]         = int(n.id) 
            dict["name"]       = n.name
            dict["timeoffset"] = request.POST['Timeoffset']
            dict["image"]      = n.fuserphoto.path
            dict["type"]       = n.usertype
        userid                 = dict["id"]
        usertype               = dict["type"]
        dict["title"]          = ""
        dict["phone"]          = ""
        dict["cellphone"]      = ""
        # Update User Table
        udict                  = {}
        udict["lastlogin"]     = datetime.datetime.now()
        udict["islogin"]       = 1
        udict["timedelay"]     = dict["timeoffset"]
        User.objects.filter(id = userid).update(**udict)
        dealerlist             = []   
        if usertype == 1:
            dealer             = User_dealer.objects.all()
            for n in dealer:
                dealerlist.append(n.id)
        else:
            dealer             = User_dealer.objects.filter(userid = userid)       
            for n in dealer:
                dealerlist.append(n.dealerid)
        
        request.session["userinfo"]   = dict
        request.session["dealerlist"] = dealerlist
        url        = reverse('dashboard_landing')
        return HttpResponseRedirect(url)
    
    def logout(self,request):
        if 'userinfo' in request.session:
            user = base(request).getUserobject()
            user.islogin = 0
            user.save()
            del request.session['userinfo']
            del request.session['dealerlist']
        return base(request).redirectloginpage()         
                  