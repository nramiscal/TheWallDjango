
from django.conf.urls import url
from . import views

urlpatterns = [
    # GET methods
    url(r'^$', views.index),
    url(r'^wall$', views.wall),
    url(r'^deleteMessage/(?P<message_id>\d+)$', views.deleteMessage),
    url(r'^logout$', views.logout),


    # POST methods
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^createMessage$', views.createMessage),
    url(r'^createComment$', views.createComment),

]
