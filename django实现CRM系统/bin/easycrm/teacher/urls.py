# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django.conf.urls import url
from teacher import views

urlpatterns = [
    url(r'^$', views.teacher_index, name="teacher_index"),
    url(r'^teacher_course/(?P<class_id>\d+)$', views.teacher_course, name="teacher_course"),
    url(r'^teacher_courserecord_add/(?P<class_id>\d+)$', views.teacher_courserecord_add, name="teacher_courserecord_add"),
    url(r'^init_studyecord$', views.init_studyecord, name="init_studyecord"),
    url(r'^teacher_study/(?P<course_id>\d+)$', views.teacher_study, name="teacher_study"),
    url(r'^teacher_homework_detail/(?P<study_id>\d+)$', views.teacher_homework_detail, name="teacher_homework_detail"),
    url(r'^down/(\d+)/(\d+)/(\d+)/(\d+)/(\w+.\w+)$', views.homework_down, name="homework_down"),
]