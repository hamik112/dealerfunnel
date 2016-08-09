from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.analysis import *
from dealerfunnel.funnel.library.paginator_plugin import *
from dealerfunnel.funnel.model_plugin.customer_model import *
from dealerfunnel.funnel.model_plugin.getcustomer_model import *
import csv 
import cStringIO as StringIO
import operator
class cloudon():
    def __init__(self):
        self.menu    = 'CUSTOMER'
        self.submenu = ''
    def landing(self,request):
        base(request).base_management(self.menu)
        return base(request).template_render(Path().CUSTOMER_LANDING,{},self.menu,self.submenu,1)
    