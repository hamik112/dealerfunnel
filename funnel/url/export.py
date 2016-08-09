from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.export import *
urlpatterns = [
    url(r'^campaign/customer/(\w+)/$',export().campaign_customer,name='campaign_customer_export'),
    url(r'^leadbyid/$',export().leadbyid,name='export_lead_by_id'),
    url(r'^alllead/$',export().export_all_lead,name='export_alllead'),
]
 