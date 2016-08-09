from dealerfunnel.funnel.view.base import *
class landing():
    def __init__(self):
        self.menu    = 'LANDING'
        self.submenu = ''
    def home(self,request):
        return base(request).view_render(Path().HOME_LANDING,{},self.menu,self.submenu,2)
               