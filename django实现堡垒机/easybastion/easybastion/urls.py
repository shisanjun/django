"""easybastion URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from web.views import user, func

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', user.acc_login, name="login"),
    url(r'^login$', user.acc_login, name="login"),
    url(r'^logout$', user.acc_logout, name="logout"),
    url(r'^index$', func.index, name="index"),
    url(r'^auditlog$', func.auditlog, name="auditlog"),
    url(r'^loglist/(\d+)$', func.loglist, name="loglist"),
    url(r'^multitask$', func.multitask, name="multitask"),
    url(r'^multitask_cmd$', func.multitask_cmd, name="multitask_cmd"),
    url(r'^taskresult$', func.taskresult, name="taskresult"),
]
