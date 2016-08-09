from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.ajax import *
urlpatterns = [
    #Campaign Setup ======================
    url(r'^customer/profile/appointment/$',ajax().get_app,name='ajax_customer_profile_appointment'),
    url(r'^customer/profile/notes/$',ajax().get_note,name='ajax_customer_profile_notes'),
    url(r'^dealer/select/$',ajax().dealerselect,name='ajax_dealer_select'),
    url(r'^customer/profile/basic/$',ajax().get_customer,name='ajax_get_customer'),
    url(r'^customer/profile/socialmedia/$',ajax().get_social_media,name='ajax_social_media'),
    url(r'^dealer/map/$',ajax().dealermap,name='ajax_dealer_map'),
]
 