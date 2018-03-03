from django.shortcuts import render, HttpResponse, redirect
from crm import models
# Create your views here.
from kindadmin import kind_admin
from kindadmin.utils import table_filter, table_sort, table_search
from kindadmin import forms
from django.contrib.auth.decorators import login_required  # 需要登陆验证


@login_required
def kind_index(request):
    if request.method == "GET":
        #print(request.user.name)  # request.user.name ==>request.userprofile.name(settings中设置指明是userprofile
        role_objs = models.UserProfile.objects.filter(name=request.user.name).first()
        return render(request, "index.html", {'role_objs': role_objs})


@login_required
def table_list(request):
    return render(request, "kindadmin/table_index.html", {"table_list": kind_admin.enabled_admin})


@login_required
def table_info(request, app_name, table_name):
    import importlib
    # model_model=importlib.import_module("%s.%s" %(app_name,"models"))
    # model_obj=getattr(model_model,table_name)
    admin_class = kind_admin.enabled_admin[app_name][table_name]

    if request.method == "POST":  # action来了
        selectd_ids = request.POST.get("select_ids")
        action = request.POST.get("action")

        if selectd_ids:
            selected_objs = admin_class.model.objects.filter(id__in=selectd_ids.split(','))
        else:
            raise KeyError("no object selected")

        if hasattr(admin_class, action):
            action_func = getattr(admin_class, action)
            request._admin_action=action
            return action_func(admin_class, request, selected_objs)

    object_list, filter_conditions = table_filter(request, admin_class)  # 过滤后的结果
    object_list, order_by_key = table_sort(request, object_list)  # 排序后的结果
    object_list = table_search(request, admin_class, object_list)  # 搜索框
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    paginator = Paginator(object_list, admin_class.list_per_page)  # 分页，每页显示3条
    page = request.GET.get("page")  # 页面返回的页码
    try:
        query_set = paginator.page(page)
    except PageNotAnInteger:  # 页码不是整数，返回第一页
        query_set = paginator.page(1)
    except EmptyPage:  # 页码最后一页
        query_set = paginator.page(paginator.num_pages)

    return render(request, "kindadmin/table_info.html",
                  {"admin_class": admin_class,
                   "query_set": query_set,
                   "filter_conditions": filter_conditions,  # 过滤条件
                   "order_by_key": order_by_key,
                   "previous_orderby": request.GET.get("o") or '',  # 上一页或者一下页需要排序条件。如果GET为None返回为空
                   "serach_text": request.GET.get("_q") or '',  # 上次搜索框查询的值
                   })


@login_required
def table_change(request, app_name, table_name, nid):

    admin_class = kind_admin.enabled_admin[app_name][table_name]
    model_form_class = forms.create_model_form(request, admin_class)  # 动态生成表单

    obj = admin_class.model.objects.filter(id=nid).first()

    if request.method == "POST":
        form_obj = model_form_class(request.POST, instance=obj)
        #这里为什么不直接用request.POST,因为request.POST是不可改变的会报This QueryDict instance is immutable
        if form_obj.is_valid():
            form_obj.save()
            return redirect("/kindadmin/%s/%s" %(app_name, table_name))

    elif request.method == "GET":

        form_obj = model_form_class(instance=obj)  # 初始化表单值

    return render(request, "kindadmin/table_change.html", {"form_obj": form_obj,
                                                           "admin_class": admin_class,
                                                           "app_name": app_name,
                                                           "table_name": table_name,
                                                           })


@login_required
def table_add(request, app_name, table_name):
    admin_class = kind_admin.enabled_admin[app_name][table_name]
    admin_class.is_add_form=True
    model_form_class = forms.create_model_form(request, admin_class)  # 动态生成表单

    if request.method == "POST":
        form_obj = model_form_class(request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect(request.path_info.replace("/add/", ""))

    elif request.method == "GET":

        form_obj = model_form_class()  # 初始化表单值

    return render(request, "kindadmin/table_add.html", {"form_obj": form_obj, "admin_class": admin_class,"table_name":table_name})


@login_required
def passwordreset(request, app_name, table_name, nid):
    admin_class = kind_admin.enabled_admin[app_name][table_name]
    model_form_class = forms.create_model_form(request, admin_class)  # 动态生成表单
    obj = admin_class.model.objects.filter(id=nid).first()
    errors = {}
    if request.method == "POST":
        _password1 = request.POST.get("password1")
        _password2 = request.POST.get("password2")
        if _password1 and _password2 and _password1 == _password2:
            obj.set_password(_password1)
            obj.save()
            return redirect(request.path.rstrip("/password.html"))
        else:
            errors["info"] = "密码为空或者密码不一致"
    return render(request, "kindadmin/password_reset.html",
                  {"obj": obj,
                   'errors': errors,
                   })


def table_delete(request, app_name, table_name, nid):
    admin_class = kind_admin.enabled_admin[app_name][table_name]
    # model_form_class = create_model_form(request, admin_class)
    objs = admin_class.model.objects.get(id=nid)  # 单客户删除的时候 要转成列表

    new_objs_list = []
    if objs:
        new_objs_list.append(objs)

    errors = {}
    if request.method == "POST":
        if not admin_class.readonly_table:
            objs.delete()
            return redirect("/kindadmin/%s/%s" % (app_name, table_name))
        errors = {"readonly_table": "The Table is Readonly!"}

    return render(request, "kindadmin/table_delete.html", {"objs": new_objs_list,
                                                           "admin": admin_class,
                                                           "app_name": app_name,
                                                           "table_name": table_name,
                                                           "errors": errors})
