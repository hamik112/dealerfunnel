from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.dealership import *
from dealerfunnel.funnel.view.campaign_setup import *
from dealerfunnel.funnel.view.campaign import *
urlpatterns = [
    url(r'^$',dealership().landing,name='dealership_landing'),
    url(r'^setup/$',dealership().setup,name='dealership_setup'),
    url(r'^setup/upload/$',dealership().setupform,name='dealership_setup_upload'),
    url(r'^setup/edit/$',dealership().editsetup,name='dealership_setup_edit'),
    url(r'^setup/edit/upload/$',dealership().editupload,name='dealership_setup_edit_upload'),
    url(r'^setup/delete/$',dealership().delete_dealership,name='dealership_delete'),
    url(r'^setup/campaign/$',campaign().dealership_setup,name='dealership_setup_campaign'),
    url(r'^json/dealerinfo/$',dealership().jsondealerinfo,name='dealer_json_info'),
]
 