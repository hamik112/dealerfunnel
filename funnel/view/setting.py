from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.campaign_model import *
import json
import datetime
class setting():
    def __init__(self):
        self.menu    = 'setting'
        self.submenu = ''
    @loginrequired
    def account_update(self,request):
        userid            = int(request.POST["userid"])
        dict              = {}
        dict["email"]     = request.POST["email"]
        dict["password"]  = request.POST["password"]
        base_model().insert(User.objects.get(id = userid),dict,1)
        url               = reverse('setting_account')
        return HttpResponseRedirect(url)
    @loginrequired
    def profile_update(self,request):
        userid            = int(request.POST["userid"])
        dict              = {}
        dict["name"]      = request.POST["name"]
        dict["title"]     = request.POST["title"]
        dict["phone"]     = commonfunction().phone_validation(request.POST["phone"])
        dict["cellphone"] = commonfunction().phone_validation(request.POST["cellphone"])
        if 'logo' in request.FILES:
            dict["fuserphoto"] = imageupload().set('logo',Path().DEALERSHIP_LOGO,request,Media_image())
        base_model().insert(User.objects.get(id = userid),dict,1)
        
        url               = reverse('setting_account')
        return HttpResponseRedirect(url)  
    @loginrequired
    def landing(self,request):
        user  = base(request).getUserobject()
        dict  = {}
        dict["password"]   = user.password
        dict["image"]   = user.fuserphoto.path
        dict["id"]   = user.id
        dict["name"] = user.name
        dict["email"] = user.email
        if user.title is None:
            dict["title"] = ""
        else:
            dict["title"] = user.title
        
        if user.phone is None:
            dict["phone"] = ""
        else:
            dict["phone"] = user.phone
        
        if user.cellphone is None:
            dict["phone"] = ""
        else:
            dict["cellphone"] = user.cellphone
        
        return base(request).view_render(Path().SETTINGNLANDING,{"user":dict},self.menu,self.submenu,2)
    