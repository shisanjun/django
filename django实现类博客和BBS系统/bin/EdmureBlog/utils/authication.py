# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django.shortcuts import redirect
from django.urls import reverse
from repository import models
def login(func):
    """
    #登陆验证装饰器
    :param func:
    :return:
    """
    def wrapper(*args,**kwargs):
        #用户是否登陆成功
        request=args[0]
        if request.session.get("is_login"):
            return func(*args,**kwargs)
        else:
            return redirect(reverse("login"))
    return wrapper

def auth(func):
    """
    #登陆验证装饰器
    :param func:
    :return:
    """
    def wrapper(*args,**kwargs):
        #用户是否登陆成功
        request=args[0]
        if request.session.get("is_login"):
            user_obj=models.UserInfo.objects.filter(username=request.session.get("username")).first()
            # if request.method=="POST":
            try:
                request.session["blog_id"]=user_obj.blog.nid
            except:
                return redirect(reverse("base_info"))
            return func(*args,**kwargs)
        else:
            return redirect(reverse("login"))
    return wrapper