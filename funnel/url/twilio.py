from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.twiliophone import *
urlpatterns = [
    url(r'^searchbox/$',twiliophone().searchbox,name='twilio_searchbox'),
    url(r'^searchnumber/$',twiliophone().searchphone,name='twilio_searchphone'),
    url(r'^buynumber/$',twiliophone().buynumber,name='twilio_buynumber'),
    url(r'^releasenumber/$',twiliophone().releasenumber,name='twilio_releasenumber'),
    url(r'^callcenter/$',twiliophone().callcenter,name='twilio_callcenter'),
]
 