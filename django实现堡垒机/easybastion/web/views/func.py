# -*- coding:utf-8 -*-
__author__ = 'shisanjun'
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
import os
import json
from repository import models
from backend.multitask_mgr import MultiTaskManage

@login_required
def index(request):
    return render(request, "index.html")

@login_required
def auditlog(request):
    """
    日志按日期显示
    :param request:
    :return:
    """
    log_date_lists=os.listdir(settings.AUDIT_LOG_IDR)

    return render(request,"auditlog.html",{"log_date_lists":log_date_lists})

@login_required
def loglist(request,date_str):
    log_list=os.listdir(os.path.join(settings.AUDIT_LOG_IDR,date_str))
    session_lists=[]
    #取出所有的session_id
    for session_tmp in log_list:
        session_lists.append(session_tmp.split("_")[1])
    session_objs=models.Sessions.objects.filter(id__in=session_lists)
    return render(request,"loglist.html",
                  {"session_objs":session_objs,
                   "date_str":date_str})

@login_required
def multitask(request):
    return render(request,"multitask_cmd.html")

@login_required
def multitask_cmd(request):
    ret={"status":False,"data":None,"error":None}
    task_obj=MultiTaskManage(request)
    if task_obj.getTask():
        ret["status"]=True
        ret["data"]="执行成功等待结果"
    else:
        ret["error"]="执行出错"
    return HttpResponse(json.dumps(ret))