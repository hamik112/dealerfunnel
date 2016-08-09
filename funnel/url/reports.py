from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.reports import *
from dealerfunnel.funnel.view.report_roi import *
from dealerfunnel.funnel.view.marketanalysis import *
from dealerfunnel.funnel.view.historical_report import *
urlpatterns = [
    url(r'^roi/$',reportroi().landing,name='reports_roi'),
    url(r'^roi/ajax/$',reportroi().ajax,name='reports_roi_ajax'),
    url(r'^roi/details/$',reportroi().details,name='reports_details'),
    url(r'^roi/downloadcsv/$',reportroi().downloadcsv,name='reports_roi_downloadcsv'),
    url(r'^marketanalysis/$',marketanalysis().landing,name='reports_marketanalysis'),
    url(r'^marketanalysis/ajax/$',marketanalysis().ajax,name='reports_marketanalysis_ajax'),
    url(r'^marketanalysis/paginajax/$',marketanalysis().ajax_market_analysis_pagin,name='reports_marketanalysis_paginajax'),
    url(r'^marketanalysis/ajax/marketbreakdown/$',marketanalysis().marketbreakdown,name='reports_marketbreakdown'),
    url(r'^marketanalysis/ajax/box/$',marketanalysis().analysisbox,name='reports_marketanalysis_box'),
    url(r'^marketanalysis/ajax/topzipcode/$',marketanalysis().topzipcode,name='reports_marketanalysis_topzipcode'),
    url(r'^marketanalysis/ajax/toptradein/$',marketanalysis().toptradein,name='reports_marketanalysis_toptradein'),
    url(r'^historical/$',historicalreport().landing,name='reports_historical'),
    url(r'^print/lead/$',reports().printlead,name='reports_print_lead'),
]
 