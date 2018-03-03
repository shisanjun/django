# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django.conf.urls import url,include
from crm import views
urlpatterns = [
    #url(r'^$',views.index,name="index")
    url(r"^customer/(?P<nid>\d+)/enroll/",views.enrollment,name="enrollment"),
    url(r"^customer/registion/(?P<nid>\d+)/",views.registion,name="registion"),
    url(r"^customer/payment/(?P<enroll_id>\d+)/",views.payment,name="payment"),
    url(r"^customer/contract_review/(?P<enroll_id>\d+)/",views.contract_review,name="contract_review"),
    url(r"^customer/enroll_rejection/(?P<enroll_id>\d+)/",views.enroll_rejection,name="enroll_rejection"),
]
