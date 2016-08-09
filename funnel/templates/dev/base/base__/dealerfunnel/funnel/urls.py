from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dealerfunnel import settings
from dealerfunnel.funnel.view.landing import *
from dealerfunnel.funnel.view.dashboard import *
from dealerfunnel.funnel.view.campaign import *
from dealerfunnel.funnel.view.customer import *
from dealerfunnel.funnel.view.leads import *
from dealerfunnel.funnel.view.dealership import *
from dealerfunnel.funnel.view.user import *
from dealerfunnel.funnel.view.campaign_setup import *
from dealerfunnel.funnel.view.reports import *
from dealerfunnel.funnel.view.iframe import *
from dealerfunnel.funnel.view.marketanalysis import *
from dealerfunnel.funnel.view.debug import *
from dealerfunnel.funnel.view.modal import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dealerfunnel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$',landing().home,name='home'),
    #DASHBOARD =============
    url(r'^dashboard/$',dashboard().landing,name='dashboard_landing'),
    url(r'^dashboard/dealerpage/$',dashboard().dealerpage,name='dashboard_dealerpage'),
    url(r'^dashboard/datefilter/$',dashboard().datefilter,name='dashboard_datefilter'),
    
    #CAMPAIGN  =============
    url(r'^campaign/$',campaign().landing,name='campaign_landing'),
    url(r'^campaign/statuschange/$',campaign().status_change,name='campaign_statuschange'),
    #CUSTOMER  =============
    url(r'^customer/$',customer().landing,name='customer_landing'),
    url(r'^customer/dealerpage/$',customer().dealerpage,name='customer_dealerpage'),
    url(r'^customer/paginfilter/$',customer().paginfilter,name='customer_paginfilter'),
    url(r'^customer/profile/$',customer().profile,name='customer_profile'),
    url(r'^customer/downloadcsv/$',customer().downloadcsv,name='customer_downloadcsv'),
    #LEADS  =============
    url(r'^leads/$',leads().landing,name='leads_landing'),
    #Dealership ======================
    url(r'^dealership/$',dealership().landing,name='dealership_landing'),
    url(r'^dealership/setup/$',dealership().setup,name='dealership_setup'),
    url(r'^dealership/setup/upload/$',dealership().setupform,name='dealership_setup_upload'),
    url(r'^dealership/setup/edit/$',dealership().editsetup,name='dealership_setup_edit'),
    url(r'^dealership/setup/delete/$',dealership().delete_dealership,name='dealership_delete'),
    url(r'^dealership/setup/campaign/$',campaign().dealership_setup,name='dealership_setup_campaign'),
    #Reports ======================
    url(r'^reports/historical/$',reports().historical,name='reports_historical'),
    url(r'^reports/roi/$',reports().roi,name='reports_roi'),
    #User ======================
    url(r'^user/$',user().landing,name='user_landing'),
    #Campaign Setup ======================
    url(r'^campaign/setup/$',campaign_setup().landing,name='campaign_setup'),
    url(r'^campaign/setup/searchfilter/$',campaign_setup().searchresult,name='campaign_setup_searchfilter'),
    url(r'^campaign/setup/tabfllter/$',campaign_setup().tabfilterview,name='campaign_setup_tabfilter'),
    url(r'^campaign/setup/paginsearchfilter/$',campaign_setup().paginsearch,name='campaign_setup_paginsearchfilter'),
    url(r'^campaign/setup/select/customer/$',campaign_setup().selectcustomer,name='campaign_setup_select_customer'),
    url(r'^campaign/setup/select/customer/range/$',campaign_setup().select_range,name='campaign_setup_select_customer_range'),
    url(r'^campaign/setup/select/customer/toggleselection/$',campaign_setup().toggleselection,name='campaign_setup_select_customer_toggleselection'),
    url(r'^campaign/setup/build/$',campaign_setup().build_campaign,name='campaign_setup_build_campaign'),
    
    #Iframe
    url(r'^iframe/map/$',iframe().map,name='user_landing'),
    
    #Debug ======================
    url(r'^debugform/$',debug().landing,name='debug_landing'),
    #Market analysis
    url(r'^reports/marketanalysis/$',marketanalysis().landing,name='reports_marketanalysis'),
    url(r'^reports/marketanalysis/ajax/$',marketanalysis().ajax,name='reports_marketanalysis_ajax'),
    url(r'^reports/marketanalysis/paginajax/$',marketanalysis().ajax_market_analysis_pagin,name='reports_marketanalysis_paginajax'),
    
    #Modal
    url(r'^modal/customer/$',modal().customer,name='customer_modal'),
    
    
    
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()