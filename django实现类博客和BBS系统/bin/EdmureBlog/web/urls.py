"""EdmureBlog URL Configuration

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
from .views import home
from .views import account

urlpatterns = [
    url(r'^$', home.index,name="index"),
    url(r'^login.html$', account.login,name="login"),
    url(r'^logout.html$', account.logout,name="logout"),
    url(r'^register.html$', account.register,name="register"),
    url(r'^check_code.html$', account.check_code),
    url(r'^include/menu.html$', home.menu,name="menu"),
    url(r'^(?P<site>\w+).html$', home.home,name="home"),
    url(r'^(?P<site>\w+)/(?P<condition>((tag)|(date)|(category)))/(?P<val>\d+).html', home.filter),
    url(r'^(?P<site>\w+)/(?P<nid>\d+).html', home.detail),
    url(r'^article/replay.html$', home.replay_article,name="replay_article"),
    url(r'^article/replay_otheruser.html$', home.replay_otheruser,name="replay_otheruser"),
    url(r'^article/up.html$', home.up_article,name="up_article"),
    url(r'^article/down.html$', home.down_article,name="down_article"),
    url(r'^article/show-(?P<article_id>\d+).html$', home.show_article,name="show_article"),
    url(r'^fans/add.html$', home.fans_add,name="fans_add"),
    url(r'^fans/cancel.html$', home.fans_cancel,name="fans_cancel"),

]
