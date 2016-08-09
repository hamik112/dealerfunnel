from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.appointment import *
urlpatterns = [
    #Campaign Setup ======================
    url(r'^activecampaign/$',appointment().activecampaign,name='activecampaign'),
    url(r'^lead/$',appointment().getLead,name='appointmnet_lead'),
    url(r'^box/$',appointment().getBox,name='appointmnet_box'),
    url(r'^pagin/$',appointment().pagin,name='appointmnet_pagin'),
    url(r'^labelchange/$',appointment().labelchange,name='appointmnet_labelchange'),
    url(r'^appstatuschange/$',appointment().appstatuschange,name='appointmnet_status_change'),
    url(r'^modalnotes/$',appointment().notemodal,name='appointmnet_notemodal'),
    url(r'^addnotes/$',appointment().addnotes,name='appointmnet_addnotes'),
    url(r'^reschedulemodal/$',appointment().reschedulemodal,name='appointmnet_reschedulemodal'),
    url(r'^savereschedule/$',appointment().savereschedule,name='appointmnet_savereschedule'),
    url(r'^ajaxcalenderview/$',appointment().ajaxcalenderview,name='appointmnet_ajaxcalenderview'),
]