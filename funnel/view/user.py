from dealerfunnel.funnel.view.base import *
import datetime
class user():
    def __init__(self):
        self.menu    = 'USER'
        self.submenu = ''
    @loginrequired
    def deleteuser(self,request):
        userid            = request.GET['uid']
        user              = User.objects.get(keyid = userid)
        dealer_user       = User_dealer.objects.filter(id = user.id)
        for n in dealer_user:
            n.delete()
        user.delete()
        url               = reverse('user_landing')
        return HttpResponseRedirect(url)     
    @loginrequired
    def updateuser(self,request):
        dict              = {}
        dict["name"]      = request.POST["name"]
        dict["email"]     = request.POST["email"]
        dict["password"]  = request.POST["password"]
        dict["usertype"]  = request.POST["utype"]
        userid            = int(request.POST['userid'])
        if 'logo' in request.FILES:
            dict["fuserphoto"] = imageupload().set('logo',Path().DEALERSHIP_LOGO,request,Media_image())
        base_model().insert(User.objects.get(id = userid),dict,1)
        pusertype         = int(request.POST["pusertype"])
        usertype          = int(request.POST["utype"])
        if pusertype == 1:
            dealer_user   = User_dealer.objects.filter(userid = userid)
            for n in dealer_user:
                n.delete() 
        if usertype == 1:
           dealerlist     = request.POST.getlist('dealership[]')
           for n in dealerlist:
               base_model().insert(User_dealer(),{"userid":userid,"dealerid":n},1)         
        
        url               = reverse('user_landing')
        return HttpResponseRedirect(url)    
    @loginrequired
    def editusermodal(self,request):
        userid  = int(request.GET['userid'])
        user    = User.objects.get(id = userid)
        dealer  = Dealer.objects.all()
        for n in dealer:
            dealerid = int(n.id)
            userdealer = User_dealer.objects.filter(userid = userid).filter(dealerid = dealerid).count()
            if userdealer == 0:
                n.selected = 0
            else:
                n.selected = 1    
        return base(request).view_render(Path().USER_EDIT,{"user":user,"dealer":dealer},self.menu,self.submenu,2) 
    @loginrequired
    def createuser(self,request):
        dealerlist        = request.POST.getlist('dealership[]')
        dict              = {}    
        dict["name"]      = request.POST["name"]
        dict["email"]     = request.POST["email"]
        dict["password"]  = request.POST["password"]
        dict["fusertype"] = usertype_lookup.objects.get(id=(int(request.POST["utype"]) + 1))
        dict["lastlogin"] = datetime.datetime.now()
        dict["rdate"]     = datetime.datetime.now()
        dict["islogin"]   = 2
        if 'logo' in request.FILES:
            dict["fuserphoto"] = imageupload().set('logo',Path().DEALERSHIP_LOGO,request,Media_image())
        else:
            dict["fuserphoto"] = Media_image.objects.get(id=1)
        id = base_model().insert(User(),dict,1)
        base_model().setkeyid(User.objects.get(id = id))
        usertype          = int(request.POST["utype"])
        if usertype == 1:
           dealerlist     = request.POST.getlist('dealership[]')
           for n in dealerlist:
               base_model().insert(User_dealer(),{"userid":id,"dealerid":n},1)   
        
        url               = reverse('user_landing')
        return HttpResponseRedirect(url) 
    @loginrequired
    def create_modal(self,request):
        dealer   = Dealer.objects.all()
        return base(request).view_render(Path().USER_CREATE_MODAL,{"domin":Path().Domain,"dealer":dealer},self.menu,self.submenu,2)
    @loginrequired
    def user_check_email(self,request):
        dict   = {"isemail":0} 
        userid = request.GET['userid']
        email  = request.GET['email']  
        emailcount = User.objects.filter(email = email).count()
        if userid == 'N':
            if emailcount == 1:
                dict["isemail"] = 1
        else:
            if emailcount == 2:
                dict["isemail"] = 1
                        
            
    @loginrequired        
    def landing(self,request):
        user = User.objects.all()
        baseclass = base(request)
        baseclass.isdealerlist = 0
        return baseclass.template_render(Path().USER_LANDING,{"domin":Path().Domain,"user":user},self.menu,self.submenu,2)
               