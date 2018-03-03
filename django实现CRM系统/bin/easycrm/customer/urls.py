# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django.conf.urls import url
from customer import views
urlpatterns = [
    url(r'^$',views.customer,name="customer"),
     url(r'^tag$',views.tags,name="tags"),
]