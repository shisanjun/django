# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django.db.models import Q
def table_filter(request,admin_class):
    """
    进行条件数据过滤并返回数据
    """
    filter_conditions={}
    for k,v in request.GET.items():
        if k=="page" or k=="o" or k=="_q":#保刘分页，相当于page是分页关键词
            continue
        if v :
            filter_conditions[k]=v
    return admin_class.model.objects.filter(**filter_conditions).order_by("-id"),filter_conditions #filter_conditions返回给前端做选择的默认值


def table_sort(request,objs):
    order_by_key=request.GET.get("o")

    if order_by_key:
        res=objs.order_by(order_by_key)
        if order_by_key.startswith("-"):
            order_by_key=order_by_key.strip("-")
        else:
            order_by_key="-%s"%order_by_key
    else:
        res=objs
    return res,order_by_key


def table_search(request,admin_class,object_list):
    serarch_key=request.GET.get("_q","") #没有返回空
    q_obj=Q()
    q_obj.connector="OR"
    for column in admin_class.search_fields:
        q_obj.children.append(("%s__contains"%column,serarch_key))

    return  object_list.filter(q_obj)

