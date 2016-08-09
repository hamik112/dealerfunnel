from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.response.response import *
urlpatterns = [
    #Campaign Setup ======================
    url(r'^lookup/$',responseapi().lookbarcode,name='response_lookup'),
    url(r'^year/$',responseapi().getyear,name='response_allyear'),
    url(r'^make/$',responseapi().getmake,name='response_make'),
    url(r'^model/$',responseapi().getmodel,name='response_model'),
    url(r'^dealerlatlng/$',responseapi().getdealerlatlng,name='response_dealerlatlng'),
    url(r'^webresponse/$',responseapi().webresponse,name='response_web_response'),
]
 