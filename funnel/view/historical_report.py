from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.analysis import *
from dealerfunnel.funnel.library.paginator_plugin import *
from dealerfunnel.funnel.library.common import *
import json 
class historicalreport():
    def __init__(self):
        self.menu    = ''
        self.submenu = ''
    
    
    @loginrequired        
    def landing(self,request):
        # This base function need to call for all url
        base(request).base_management(self.menu)
        self.menu    = 'HISTORICAL'
        return base(request).template_render(Path().HISTORICAL_LANDING,{},self.menu,self.submenu,1)