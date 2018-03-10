# -*- coding:utf-8 -*-
__author__ = 'shisanjun'
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.conf import settings
import os
import json
from repository import models
from backend.multitask_mgr import MultiTaskManage
import time


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
    log_date_lists = os.listdir(settings.AUDIT_LOG_IDR)

    return render(request, "auditlog.html", {"log_date_lists": log_date_lists})


@login_required
def loglist(request, date_str):
    log_list = os.listdir(os.path.join(settings.AUDIT_LOG_IDR, date_str))
    session_lists = []
    # 取出所有的session_id
    for session_tmp in log_list:
        session_lists.append(session_tmp.split("_")[1])
    session_objs = models.Sessions.objects.filter(id__in=session_lists)
    return render(request, "loglist.html",
                  {"session_objs": session_objs,
                   "date_str": date_str})


@login_required
def multitask(request):
    return render(request, "multitask_cmd.html")


@login_required
def multitask_cmd(request):

    ret = {"status": False, "task_id":None,"data": None, "error": None}
    task_obj = MultiTaskManage(request)
    task_id = task_obj.getTask()

    if task_id:
        ret["status"] = True
        ret["task_id"]=task_id
        ret["data"] = list(models.TaskLogDetail.objects.filter(task_id=task_id).values_list("id",
                                                                                            "bind_host__host__ip_addr",
                                                                                            "result",
                                                                                            "status"))
    else:
        ret["error"] = "执行出错"

    return HttpResponse(json.dumps(ret))


def taskresult(request):
    task_id=request.GET.get("task_id")

    data = list(models.TaskLogDetail.objects.filter(task_id=task_id).values("id",  "result", "status"))

    return HttpResponse(json.dumps(data))