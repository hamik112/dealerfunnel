from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.customer import customer,setappointment,setnotes
urlpatterns = [
    url(r'^$',customer().landing,name='customer_landing'),
    url(r'^paginfilter/$',customer().paginfilter,name='customer_paginfilter'),
    url(r'^dealerpage/$',customer().dealerpage,name='customer_dealerpage'),
    url(r'^profile/$',customer().profile,name='customer_profile'),
    url(r'^downloadcsv/$',customer().downloadcsv,name='customer_downloadcsv'),
    url(r'^setup/app/$',setappointment().postapp,name='app_setup'),
    url(r'^setup/note/$',setnotes().postnotes,name='note_setup'),
]
 