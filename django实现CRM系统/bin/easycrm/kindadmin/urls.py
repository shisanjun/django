# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django.conf.urls import url
from kindadmin import views

urlpatterns = [
    url(r'^$', views.kind_index, name="kind_index"),
    url(r'^table_list$', views.table_list, name="table_list"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)$', views.table_info, name="table_info"),  # 传递app_name和table_name
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<nid>\d+)/change/$', views.table_change, name="table_change"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<nid>\d+)/delete/$', views.table_delete, name="table_delete"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)/(?P<nid>\d+)/change/password.html$', views.passwordreset,
        name="passwordreset"),
    url(r'^(?P<app_name>\w+)/(?P<table_name>\w+)/add/$', views.table_add, name="table_add"),

]
