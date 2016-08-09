from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.analysis import *
from dealerfunnel.funnel.library.paginator_plugin import * 
class iframe():
    def __init__(self):
        self.menu    = 'CUSTOMER'
        self.submenu = ''
    def map(self,request):
        # Check Login Authentication
        if base(request).isnotauthentication():
            return base(request).redirectloginpage()
        
        lat  = request.GET['lat']
        lng  = request.GET['lng']
        return base(request).view_render(Path().IFRAME_MAP,{"lat":lat,"lng":lng},self.menu,self.submenu,1)