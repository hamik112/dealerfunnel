from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.dashboard import *
urlpatterns = [
    url(r'^$',dashboard().landing,name='dashboard_landing'),
    url(r'^dealerpage/$',dashboard().dealerpage,name='dashboard_dealerpage'),
    url(r'^datefilter/$',dashboard().datefilter,name='dashboard_datefilter'),
    url(r'^ajax_customer_compare/$',dashboard().ajax_customer_compare,name='ajax_customer_compare'),
    url(r'^ajax_chart/$',dashboard().ajax_chart,name='ajax_chart'),
]
 