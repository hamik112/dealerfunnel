from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.setting import *
urlpatterns = [
    url(r'^account/$',setting().landing,name='setting_account'),
    url(r'^profile/update/$',setting().profile_update,name='setting_profile_update'),
    url(r'^account/update/$',setting().account_update,name='setting_account_update'),
]
 