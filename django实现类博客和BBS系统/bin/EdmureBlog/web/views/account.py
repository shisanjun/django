#!/usr/bin/env python
# -*- coding:utf-8 -*-
from io import BytesIO
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import  redirect
from utils.check_code import create_validate_code
from django.core.exceptions import ValidationError
from web import forms
from django.urls import reverse
import json
from repository import models
def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


def login(request):
    """
    登陆
    :param request:
    :return:
    """
    if request.method=="GET":
        obj=forms.LoginForm()
        return render(request, 'login.html',{"obj":obj})
    if request.method == "POST":
        obj=forms.LoginForm(request.POST)
        if obj.is_valid():
            if request.session['CheckCode'].lower() == request.POST.get('check_code').lower():
                    request.session["username"]=obj.cleaned_data.get("username")
                    request.session["is_login"]=True
                    if obj.cleaned_data.get("cookietime"):
                        request.session.set_expiry(30*24*60*60)
                    return redirect(reverse("index"))
            else:
                return render(request, 'login.html',{"obj":obj})
        else:
            return render(request, 'login.html',{"obj":obj})


class JsonCunstomEncode(json.JSONEncoder):
    def default(self, field):
        if isinstance(field,ValidationError):
            return {"code":field.code,"message":field.message}
        else:
            return json.JSONEncoder.default(self,field)

def register1(request):
    """
    注册
    :param request:
    :return:
    """
    ret={"status":False,"error":None,"data":None}
    if request.method=="GET":
        register_obj=forms.RegisterForm()
        return render(request, 'register.html',{"register_obj":register_obj})
    elif request.method=="POST":
        register_obj=forms.RegisterForm(request.POST)
        if register_obj.is_valid():
            ret["status"]=True
            ret["data"]=register_obj.cleaned_data
        else:
            ret["error"]=register_obj.errors.as_data()
            # print(type(register_obj.errors.as_json()))
            # print(type(register_obj.errors.as_data()))
        result=json.dumps(ret,cls=JsonCunstomEncode)
        #不能使用render，使用render返回数据,前端var data1=JSON.parse(arg)转换报错。可以使用HttpResponse直接返回数据
        #return render(request, 'register.html',{"result":result})
        return HttpResponse(result)

def register(request):
    """
    注册
    :param request:
    :return:
    """
    ret={"status":False,"error":None,"data":None}
    if request.method=="GET":
        register_obj=forms.RegisterForm()
        return render(request, 'register.html',{"register_obj":register_obj})
    elif request.method=="POST":
        register_obj=forms.RegisterForm(request.POST)
        if register_obj.is_valid():
            reverse_url=reverse("register")
            if request.session['CheckCode'].lower() == request.POST.get('check_code').lower():

                username=register_obj.cleaned_data.get("username")
                email=register_obj.cleaned_data.get("email")
                password=register_obj.cleaned_data.get("password")
                user_obj=models.UserInfo.objects.create(username=username,email=email,password=password)
                if user_obj:
                    request.session.clear()
                    request.session["username"]=username
                    request.session["is_login"]=True
                    ret["status"]=True
                    ret["data"]=register_obj.cleaned_data
                    #成功js跳转到base_info.html
        else:
            ret["error"]=register_obj.errors.as_json()
        result=json.dumps(ret)
        #不能使用render，使用render返回数据,前端var data1=JSON.parse(arg)转换报错。可以使用HttpResponse直接返回数据
        #return render(request, 'register.html',{"result":result})
        return HttpResponse(result)

def logout(request):
    """
    注销
    :param request:
    :return:
    """
    if request.method=="GET":
        #清除该用户所有的session
        request.session.clear()
        #反转到login页面
        reverse_login=reverse("login")
        return redirect(reverse_login)
