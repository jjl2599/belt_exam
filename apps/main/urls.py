from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^users$', views.create_user),
    url(r'^success$', views.success),
    url(r'^home$', views.home),
    url(r'^sessions$', views.login_user),
    url(r'^appointments$', views.appointments),
    url(r'^editpage/(?P<id>\d+)$', views.editpage),
    url(r'^edit/(?P<id>\d+)$', views.edit),
    url(r'^delete/(?P<id>\d+)$', views.delete),
]
