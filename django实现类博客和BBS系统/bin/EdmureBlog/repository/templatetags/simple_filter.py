# _*_ coding:utf-8 _*_
__author__ = "shisanjun"

from django import template
from repository import models
from django.utils.safestring import mark_safe
register=template.Library()

@register.filter
def my_article_type(v1):
    type_choices = models.Article.type_choices
    for item in type_choices:
        if item[0]==v1:
            return item[1]

@register.filter
def select_tags(v1,v2):
    """
    选择文章的tags
    :param v1:
    :param v2:
    :return:
    """
    for v in v2:
        if v1==v.nid:
            return True
    return False

@register.simple_tag
def render_error_info(errors):
    """
    错误信息展示；包括__all__
    :param errors:
    :return:
    """
    error_lists=[]
    for k,v in errors.items():
        error_lists.append(v)
    return error_lists


@register.simple_tag
def blog_login_valid(request):
    res_str="""
                <div class="reply-area" style="position: relative;">
                <div style="text-align:center;line-height:200px;position: absolute;top:0;left:0;right:0;bottom: 0;background-color: rgba(255,255,255,.6)">
                    您需要登录后才可以回帖 <a href="/login.html">登录</a> | <a href="/register.html">立即注册</a>
                </div>
                <textarea  name="content" style="width: 100%;height:200px;visibility:hidden;"></textarea>
            </div>
     """

    if  request.session.get("is_login"):
        res_str="""
                <div class="reply-area" style="position: relative;">
                <textarea  name="content" style="width: 100%;height:200px;"></textarea>
            </div>
     """
    return mark_safe(res_str)

@register.simple_tag
def truncate_str_twenty(truncte_str):
   # print(truncte_str[:20])
    return truncte_str[:20]