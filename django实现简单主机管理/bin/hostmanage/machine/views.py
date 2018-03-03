from django.shortcuts import render,redirect,HttpResponse
from machine.models import HostGroup,Host,UserGroup,User
from datetime import datetime
import json
# Create your views here.




def login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method=="GET":
        return  render(request,"login.html")

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        cookie_time=request.POST.get("cookietime")
        obj=User.objects.filter(username=username,password=password).first()
        #登陆验证
        if obj is not None:
            response=redirect("/index")
            #设置登陆session时间
            if cookie_time=="1":
                request.session.set_expiry(1*24*60*60)
            elif cookie_time=="2":
                request.session.set_expiry(7*24*60*60)
            elif cookie_time=="3":
                request.session.set_expiry(30*24*60*60)
            #设置session用户名和角色
            request.session["username"]=obj.username
            request.session["role"]=obj.user_group.name
            request.session["is_login"]=True
            return response

        return render(request,"login.html")


def logout(request):
    if request.method=="GET":
        request.session.clear()
        return redirect("/login")


def auth(func):
    def inner(*args,**kwargs):
        request=args[0]
        if not request.session.get("is_login"):
            return redirect("/login")
        else:
            return func(*args,**kwargs)
    return inner



@auth #装饰器登陆
def index(request):
    """
    首页
    :param request:
    :return:
    """
    user=request.COOKIES.get("user")
    role=request.COOKIES.get("role")
    return render(request,"index.html",{"user":user,"role":role})


@auth #装饰器登陆
def host(request):
    """
    主机列表
    :param request:
    :return:
    """
    if request.method=="GET":
        hosts=Host.objects.all()
        return  render(request,"host.html",{"hosts":hosts})


@auth #装饰器登陆
def host_add(request):
    if request.method=="GET":
        host_groups=HostGroup.objects.all()
        return render(request,"host_add.html",{"host_groups":host_groups})
    if request.method=="POST":
        hostname=request.POST.get("hostname")
        ip=request.POST.get("ip")
        port=request.POST.get("port")
        cabinet=request.POST.get("cabinet")
        ctime=request.POST.get("ctime")
        hostinfo=request.POST.get("hostinfo")
        group=request.POST.get("group")

        Host.objects.create(hostname=hostname,ip=ip,port=port,cabinet=cabinet,ctime=ctime,hostinfo=hostinfo,group_id=group)
        return redirect("/machine/host")

@auth #装饰器登陆
def host_edit(request,hid):
    if request.method=="GET":
        host_obj=Host.objects.filter(id=hid).first()
        host_groups=HostGroup.objects.all()
        return render(request,"host_edit.html",{"host_obj":host_obj,"host_groups":host_groups})

    if request.method=="POST":
        hostname=request.POST.get("hostname")
        ip=request.POST.get("ip")
        port=request.POST.get("port")
        cabinet=request.POST.get("cabinet")
        ctime=request.POST.get("ctime")
        hostinfo=request.POST.get("hostinfo")
        group=request.POST.get("group")

        Host.objects.filter(id=hid).update(hostname=hostname,ip=ip,port=port,cabinet=cabinet,ctime=ctime,hostinfo=hostinfo,group_id=group)
        return  redirect("/machine/host")

@auth #装饰器登陆
def host_delete(request,hid):
    if request.method=="GET":
        host_obj=Host.objects.filter(id=hid).first()
        return render(request,"host_delete.html",{"host_obj":host_obj})

    if request.method=="POST":
        Host.objects.filter(id=hid).delete()
        return  redirect("/machine/host")

@auth #装饰器登陆
def hostgroup(request):

    if request.method=="GET":
        host_groups=HostGroup.objects.all()
        return render(request,"hostgroup.html",{"host_groups":host_groups})
    if request.method=="POST":
        groupname=request.POST.get("groupname")
        HostGroup.objects.create(name=groupname)
        return redirect("/machine/hostgroup")

@auth #装饰器登陆
def hostgroup_edit(request):

    res={"status":False}
    if request.method=="POST":
        gid=request.POST.get("gid")
        gname=request.POST.get("groupname")
        HostGroup.objects.filter(id=gid).update(name=gname)
        res={"status":True}
    res_info=json.dumps(res)
    return HttpResponse(res_info)


@auth #装饰器登陆
def hostgroup_delete(request):
    res={"status":False}
    if request.method=="POST":
        gid=request.POST.get("gid")
        obj=HostGroup.objects.filter(id=gid).delete()
        if obj:
            res={"status":True}

    res_info=json.dumps(res)
    return HttpResponse(res_info)

@auth #装饰器登陆
def user(request):
    res={"status":False}
    if request.method=="GET":
        users=User.objects.all()
        user_groups=UserGroup.objects.all()
        hosts=Host.objects.all()
        return render(request,"user.html",{"users":users,"user_groups":user_groups,"hosts":hosts})

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        gname=request.POST.get("gname")
        obj=User.objects.create(username=username,password=password,user_group_id=gname)
        if obj:
             res={"status":True}

    res_info=json.dumps(res)
    return redirect("/machine/user")


@auth #装饰器登陆
def user_edit(request):
    res={"status":False}
    if request.method=="POST":
        uid=request.POST.get("id")
        username=request.POST.get("username")
        password=request.POST.get("password")
        gname=request.POST.get("gname")
        obj=User.objects.filter(id=uid).update(username=username,password=password,user_group_id=gname)
        if obj:
            res={"status":True}
    res_info=json.dumps(res)
    return HttpResponse(res_info)


@auth #装饰器登陆
def user_delete(request):
    res={"status":False}
    if request.method=="POST":
        uid=request.POST.get("uid")
        print(uid)
        obj=User.objects.filter(id=uid).delete()
        if obj:
            res={"status":True}
    res_info=json.dumps(res)
    return HttpResponse(res_info)

@auth #装饰器登陆
def usergroup(request):
    if request.method=="GET":
        user_groups=UserGroup.objects.all()
        return render(request,"usergroup.html",{"user_groups":user_groups})

    if request.method=="POST":
        gname=request.POST.get("gname")
        obj=UserGroup.objects.create(name=gname)


        return redirect("/machine/usergroup")

@auth #装饰器登陆
def usergroup_edit(request):
    res={"status":False}
    if request.method=="POST":
        uid=request.POST.get("id")
        username=request.POST.get("username")
        password=request.POST.get("password")
        gname=request.POST.get("gname")
        obj=User.objects.filter(id=uid).update(username=username,password=password,user_group_id=gname)
        if obj:
            res={"status":True}
    res_info=json.dumps(res)
    return HttpResponse(res_info)


@auth #装饰器登陆
def usergroup_delete(request):
    res={"status":False}
    if request.method=="POST":
        uid=request.POST.get("uid")
        print(uid)
        obj=User.objects.filter(id=uid).delete()
        if obj:
            res={"status":True}
    res_info=json.dumps(res)
    return HttpResponse(res_info)

@auth #装饰器登陆
def userhost(request):
    """
    申请分配主机给用户
    :param request:
    :return:
    """
    if request.method=="GET":
        user_objs=User.objects.all()
        hostgroup_objs=HostGroup.objects.all()
        return render(request,"host2user.html",{"user_objs":user_objs,"hostgroup_objs":hostgroup_objs})
    elif request.method=="POST":
        user_id=request.POST.get("username")
        host_ip=request.POST.get("hostip")
        host_group_id=request.POST.get("hostgroup")

        user_objs=User.objects.filter(id=user_id).first()
        host_objs=Host.objects.filter(group_id=host_group_id).values("id","ip")
        tag=True
        for host_obj in host_objs:
            print(type(host_obj))
            if host_ip == host_obj.get("ip"):
                tag=False
            user_objs.hosts.add(host_obj.get("id"))

        if tag:
                try:
                    host_id=Host.objects.filter(ip=host_ip).values("id").first()
                    print(host_id)
                    user_objs.hosts.add(host_id.id)
                except:
                    pass


        return redirect("/machine/user")



