from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dealerfunnel import settings
from dealerfunnel.funnel.view.landing import *
from dealerfunnel.funnel.view.campaign import *
from dealerfunnel.funnel.view.leads import *
from dealerfunnel.funnel.view.dealership import *
from dealerfunnel.funnel.view.campaign_setup import *
from dealerfunnel.funnel.view.iframe import *
from dealerfunnel.funnel.view.debug import *
from dealerfunnel.funnel.view.modal import *
from dealerfunnel.funnel.view.ajax import *
from dealerfunnel.funnel.view.login import *
from dealerfunnel.funnel.view.jsonrequest import *
from dealerfunnel.funnel.view.appointment import *
from dealerfunnel.funnel.view.campaign_detail_page import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dealerfunnel.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^dealership/', include('dealerfunnel.funnel.url.dealership')),
    url(r'^api/',include('dealerfunnel.funnel.url.api')),
    url(r'^user/',include('dealerfunnel.funnel.url.user')),
    url(r'^twilio/',include('dealerfunnel.funnel.url.twilio')),
    url(r'^dashboard/',include('dealerfunnel.funnel.url.dashboard')),
    url(r'^customer/',include('dealerfunnel.funnel.url.customer')),
    url(r'^reports/',include('dealerfunnel.funnel.url.reports')),
    url(r'^export/',include('dealerfunnel.funnel.url.export')),
    url(r'^setting/',include('dealerfunnel.funnel.url.setting')),
    url(r'^login/',include('dealerfunnel.funnel.url.login')),
    url(r'^campaign/',include('dealerfunnel.funnel.url.campaign')),
    url(r'^$',landing().home,name='home'),
    
    #AJAX  =============
    url(r'^ajax/dealer/select/$',ajax().dealerselect,name='ajax_dealer_select'),
    
    
    #LEADS  =============
    url(r'^leads/$',leads().landing,name='leads_landing'),
    #Campaign Details Page ======================
    url(r'^selected/campaign/detail/page/$',campaigndetailpage().selected_campaign,name='selected_campaign_details_page'),
    #Iframe
    url(r'^iframe/map/$',iframe().map,name='iframe_landing'),
    #Modal
    url(r'^modal/customer/$',modal().customer,name='customer_modal'),
    #Login  =============
    url(r'^forgotpassword/$',login().forgotpassword,name='login_forgotpassword'),
    url(r'^logout/$',login().logout,name='logout'),
    url(r'^changepassword/(\w+)/$',login().changepassword,name='changepassword'),
    url(r'^changepasswordupdate/$',login().changepasswordupdate,name='changepassword_update'),
    
    
    #Setting
    
    
    #JSON
    #url(r'^json/check/useremail/$',jsonrequest().usercheckusermail,name='json_check_useremail'),
    #url(r'^json/forgotpassword/$',jsonrequest().forgotpassword,name='json_forgotpassword'),
    #Response Api
    
    # Export
    
    #Debug ======================
    #url(r'^setcampaindealer/$',randomlead().updatecampaignlead,name='updatecampaignlead'),
    #url(r'^randomlead/$',randomlead().setlead,name='randomlead'),
    url(r'^debugform/$',debug().landing,name='debug_landing'),
    url(r'^debugformt/$',debug().customerdebug,name='debug_landing'),
    url(r'^debugjquery/$',debug().testjquery,name='debug_jquery'),
    url(r'^debugformsubmit/$',debug().debugformsubmit,name='debug_debugformsubmit'),
    url(r'^scanbarcode/$',debug().scanbarcode,name='debug_scanbarcode'), 
    url(r'^checkbarcode/$',debug().checkbarcode,name='debug_checkbarcode'),
    # API
    #===========================================
    #===================================================================
    #url(r'^cloudon/$',cloudoneapi().setcloud,name='api_set_cloudone'),
    
    url(r'^appointment/$',appointment().landing,name='appointment_landing'),
    
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()