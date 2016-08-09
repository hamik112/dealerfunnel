from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.library.mail import dealerfunnelmail
import json
class jsonrequest():
    def __init__(self):
        self.menu    = ''
        self.submenu = ''
    def usercheckusermail(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        
        dict   = {"isemail":0} 
        userid = request.GET['userid']
        email  = request.GET['email']  
        emailcount = User.objects.filter(email = email).count()
        if userid == 'N':
            if emailcount == 1:
                dict["isemail"] = 1
        else:
            if emailcount == 1:
                user   = User.objects.get(id = userid)
                if user.email == email:
                    dict["isemail"] = 0
                else:
                    dict["isemail"] = 1    
        return HttpResponse(json.dumps(dict), content_type = "application/json")        
    def forgotpassword(self,request):
        email  = request.GET['email']
        emailcount = User.objects.filter(email = email).count()
        dict   = {"isemail":0}
        if emailcount == 1:
            user    = User.objects.get(email = email)
            to      = [user.email]
            keyid   = hashlib.sha224(str(user.id)).hexdigest()
            context = {"name":user.name,"key":keyid}
            base_model().insert(User.objects.get(id = user.id),{"forgottenkey":keyid},1)   
            dealerfunnelmail().forgotpassword(context,to)
            dict["isemail"] = 1    
        return HttpResponse(json.dumps(dict), content_type = "application/json")
        
            
    