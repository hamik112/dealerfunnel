from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.login import *
urlpatterns = [
    url(r'^$',login().landing,name='login_landing'),
    url(r'^jsoncheck/$',login().jsoncheck,name='login_jsoncheck'),
    url(r'^submit/$',login().submit,name='login_submit'),
]
 