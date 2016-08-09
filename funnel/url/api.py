from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.dealership import *
from dealerfunnel.funnel.view.campaign_setup import *
from dealerfunnel.funnel.view.campaign import *
from dealerfunnel.funnel.view.api.lead import *
from dealerfunnel.funnel.view.api.response import *
from dealerfunnel.funnel.view.api.report import *
from dealerfunnel.funnel.view.api.customer_note import *
from dealerfunnel.funnel.view.api.appointment import *
from dealerfunnel.funnel.view.api.lookup import *
from dealerfunnel.funnel.view.api.customer import *
from dealerfunnel.funnel.view.api.setlead import *
from dealerfunnel.funnel.view.api.cloudone import *
from dealerfunnel.funnel.view.api.campaign import *
from dealerfunnel.funnel.view.api.campaigndealer import *
from dealerfunnel.funnel.view.responseapi import *
urlpatterns = [
    # Campaign Related API
    url(r'^responsecount/$',campaignapi().response_count,name='api_response_count'),
    url(r'^getstats/$',campaignapi().getstats,name='api_campaign_getstats'),
    url(r'^getcampaignbox/$',campaignapi().campaignbox,name='api_campaign_getbox'),
    url(r'^getcampaigndate/$',campaignapi().getDate,name='api_campaign_getbox'),
    url(r'^getcampaignroimatch/$',campaignapi().getroimatch,name='api_campaign_roi_match'),
    url(r'^getallcampaignbydealer/$',api_campaigndealer().getallcampaignbydealer,name='api_get_all_campaign_by_dealer'),
    url(r'^getallcampaignbycmp/$',api_campaigndealer().getallcampaignbycmp,name='api_get_all_campaign_by_campaign'),
    url(r'^getleaddaterange/$',leadapi().getdaterange,name='api_get_lead_date_range'),
    url(r'^getresponselabel/$',leadapi().getResonponseLabel,name='api_get_response_label'),
    url(r'^getlead/$',leadapi().getLead,name='api_get_lead'),
    url(r'^getnewleadcount/$',leadapi().getNewLead,name='api_get_new_lead_count'),
    url(r'^getleadcount/$',leadapi().getLeadCount,name='api_get_lead_count'),
    url(r'^changelabel/$',leadapi().changeLabel,name='api_change_label'),
    url(r'^getcampaignbydate/$',leadapi().getCampaignList,name='api_get_campaign_by_date_range'),
    url(r'^adjustnewlead/customer/$',leadapi().adjustnewlead,name='api_adjust_new_lead'),
    url(r'^updateleadatt/$',leadapi().updateleadatt,name='api_update_lead_att'),
    #===================================================================
    url(r'^addnote/$',customernoteapi().addnote,name='api_add_note'),
    url(r'^getnotes/$',customernoteapi().getnotes,name='api_get_notes'),
    url(r'^deletenotes/$',customernoteapi().deletenotes,name='api_get_notes'),
    url(r'^updatenotes/$',customernoteapi().updatenote,name='api_update_notes'),
    url(r'^getcustomer/$',customerapi().getCustomer,name='api_get_customer'),
    #==================================================================
    url(r'^getresponseinfo/$',customerapi().getresponseinfo,name='api_get_response_info'),
    #==================================================================
    url(r'^gettopzipcode/$',api_report().getTopZipcode,name='api_get_top_zip_code'),
    url(r'^gettoptradein/$',api_report().gettoptradein,name='api_get_top_tradein'),
    url(r'^gethistoricalsaleschartdata/$',api_report().getHistoricalSalesChart,name='api_get_historical_sales_chart_data'),
    url(r'^gethistoricalservicechartdata/$',api_report().getHistoricalServiceChart,name='api_get_historical_service_chart_data'),
    #==================================================================
    url(r'^getappointment/$',appointmentapi().getAppointment,name='api_get_appointment'),
    #==================================================================
    url(r'^getmakes/$',lookupapi().getMake,name='api_get_makes'),
    url(r'^getmodels/$',lookupapi().getModels,name='api_get_models'),
    url(r'^response/$',responseapi().setresponse,name='api_response'),
    #===================================================================
    url(r'^setappointment/$',setleadapi().setApp,name='api_set_appointment'),
]
 