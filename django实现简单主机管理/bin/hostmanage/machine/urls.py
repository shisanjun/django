"""hostmanage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from machine import views
urlpatterns = [
    url(r'^host/', views.host,name="host"),
    url(r'^host_add$', views.host_add,name="host_add"),
    url(r'^host_edit-(?P<hid>\d+)', views.host_edit,name="host_edit"),
    url(r'^host_delete-(?P<hid>\d+)', views.host_delete,name="host_delete"),

    url(r'^hostgroup/', views.hostgroup,name="hostgroup"),
    url(r'^hostgroup_edit$', views.hostgroup_edit,name="hostgroup_edit"),
    url(r'^hostgroup_delete$', views.hostgroup_delete,name="hostgroup_delete"),

    url(r'^user/', views.user,name="user"),
    url(r'^user_edit$', views.user_edit,name="user_edit"),
    url(r'^user_delete$', views.user_delete,name="user_delete"),

    url(r'^usergroup/', views.usergroup,name="usergroup"),
    url(r'^usergroup_edit$', views.usergroup_edit,name="usergroup_edit"),
    url(r'^usergroup_delete$', views.usergroup_delete,name="usergroup_delete"),

    url(r'^userhost$', views.userhost,name="userhost"),
]
