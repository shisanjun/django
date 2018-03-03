# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from crm.permissions import permission_list
from django.shortcuts import redirect,HttpResponse
from django.urls import reverse
from django.core.urlresolvers import resolve
def perm_check(*args,**kwargs):
    request=args[0]
    #判断有没有登陆
    if not request.user.is_authenticated():
        return redirect(reverse("acc_login"))
    for perm_name,v in permission_list.perm_dict.items():

        url_matched=False
        if v.get("url_type")==1:#absoute url
            if v.get("url")==request.path:#绝对路径url匹配上
                url_matched=True
                print(perm_name,"absolte path")
        else:
            #把绝对的url转相对的url
            resolve_obj=resolve(request.path)
            if resolve_obj.url_name==v.get("url"):#相对url别名匹配上
                url_matched=True
                print(perm_name,"relate path")

        if  url_matched:
            if v.get("method")==request.method:#请求方法也匹配上
                args_metched=True
                for request_arg in v.get("args"):
                    print(perm_name,"method ...")
                    request_method_func=getattr(request,v["method"])
                    if request_method_func.get(request_arg):
                        args_metched=False
                if args_metched: #走到这里，权限匹配上,仅代表这个请求和这条权限的定义规则，匹配上了
                    if request.user.has_perm(perm_name):#代表有权限
                        return True
    return False



def check_permission(func):
    def wrapper(*args,**kwargs):

        if perm_check(*args,**kwargs):
            return func(*args,**kwargs)
        else:
            return HttpResponse("没有权限")

    return wrapper