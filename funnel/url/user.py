from django.conf.urls import include, url
from django.conf.urls import *
from dealerfunnel.funnel.view.user import *
urlpatterns = [
    url(r'^$',user().landing,name='user_landing'),
    url(r'^create/$',user().createuser,name='create_user'),
    url(r'^edituser/$',user().editusermodal,name='user_edituser'),
    url(r'^updateuser/$',user().updateuser,name='user_updateuser'),
    url(r'^create/modal/$',user().create_modal,name='user_create_modal'),
    url(r'^deleteuser/$',user().deleteuser,name='user_delete'),
]
 