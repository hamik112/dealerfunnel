from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.dealership import *
from dealerfunnel.funnel.view.campaign_setup import *
from dealerfunnel.funnel.view.campaign import *
from dealerfunnel.funnel.view.campaign_detail_page import *
urlpatterns = [
    #Campaign Setup ======================
    url(r'^setup/$',campaign_setup().landing,name='campaign_setup'),
    url(r'^setup/searchfilter/$',campaign_setup().searchresult,name='campaign_setup_searchfilter'),
    url(r'^setup/tabfllter/$',campaign_setup().tabfilterview,name='campaign_setup_tabfilter'),
    url(r'^setup/paginsearchfilter/$',campaign_setup().paginsearch,name='campaign_setup_paginsearchfilter'),
    url(r'^setup/select/customer/$',campaign_setup().selectcustomer,name='campaign_setup_select_customer'),
    url(r'^setup/select/customer/range/$',campaign_setup().select_range,name='campaign_setup_select_customer_range'),
    url(r'^setup/select/customer/toggleselection/$',campaign_setup().toggleselection,name='campaign_setup_select_customer_toggleselection'),
    url(r'^setup/build/$',campaign_setup().build_campaign,name='campaign_setup_build_campaign'),
    url(r'^$',campaign().landing,name='campaign_landing'),
    url(r'^statuschange/$',campaign().status_change,name='campaign_statuschange'),
    url(r'^setup/filter/budgetmonth/$',campaign().dealership_setup_budget_filter,name='campaign_setup_filter_budgetmonth'),
    url(r'^load/by/dealer/$',campaign().load_by_dealer,name='campaign_load_by_dealer'),
    url(r'^load/by/ajax/$',campaign().load_by_ajax,name='campaign_load_by_ajax'),
    url(r'^detail/page/(\w+)/(\w+)/$',campaigndetailpage().landing,name='campaign_details_page'),
    url(r'^details/selected/campaign/$',campaigndetailpage().selected_campaign,name='campaign_selected_campaign'),
    url(r'^details/ajax_roi/$',campaigndetailpage().ajax_roi,name='campaign_details_ajax_roi'),
]
 