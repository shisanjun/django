from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required

from django.urls import reverse

# Create your views here

def acc_login(request):

    ret=""
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect(reverse("index"))
        else:
            ret="邮箱或者密码不正确，请重新输入"

    return  render(request, "login.html", {"error":ret})

def acc_logout(request):
    logout(request)
    return redirect(reverse("login"))

