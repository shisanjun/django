# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django import views
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    if request.method=="GET":
        # print(request.user.name)
        #for role in request.user.user.roles.all():
        #     print(role)
        return render(request,"index.html")


def acc_login(request):

    if request.method=="POST":

        _email=request.POST.get("email")
        _password=request.POST.get("password")

        user=authenticate(email=_email,password=_password) #返回e用户对象或者None

        if user is not None:
            login(request,user)#自动会创建user session
            next_url=request.GET.get('next',"/")
            print(next_url)
            return redirect("%s"%next_url) #登陆成功后，返回原页面

    return render(request,"login.html")

def acc_logout(request):
    logout(request)#退出
    return redirect(reverse("acc_login"))