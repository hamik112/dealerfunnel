from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.modal import *
urlpatterns = [
    #Campaign Setup ======================
    url(r'^response/$',modal().responsehtml,name='modal_response'),
    
]
 