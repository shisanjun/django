# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django.conf.urls import url
from student import views

urlpatterns = [
    url(r'^$', views.student_index, name="student_index"),
    url(r'^homework/(?P<enroll_id>\d+)$', views.homework, name="homework"),
    url(r'^homework_detail/(?P<courserecord_id>\d+)$', views.homework_detail, name="homework_detail"),
]