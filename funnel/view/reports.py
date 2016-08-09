from dealerfunnel.funnel.view.base import *
from dealerfunnel.funnel.model_plugin.analysis import *
from dealerfunnel.funnel.library.paginator_plugin import * 
class reports():
    def __init__(self):
        self.menu    = ''
        self.submenu = ''
    def historical(self,request):
        self.menu    = 'HISTORICAL'
        return base(request).template_render(Path().REPORTS_HISTORICAL,{},self.menu,self.submenu,1)
    def marketanalysis(self,request):
        self.menu    = 'MARKETANALYSIS'
        return base(request).template_render(Path().REPORTS_MANALYSIS,{},self.menu,self.submenu,1)
    def roi(self,request):
        self.menu    = 'ROI'
        return base(request).template_render(Path().REPORTS_ROI,{},self.menu,self.submenu,1)
    def printlead(self,request):
        return base(request).view_render('reports/lead.html',{},self.menu,self.submenu,1)
    
                       