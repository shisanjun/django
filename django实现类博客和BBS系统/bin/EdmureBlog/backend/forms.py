# _*_ coding:utf-8 _*_
__author__ = "shisanjun"

from django import forms
from django.forms import fields
from django.core.exceptions import ValidationError
from repository import models
class BaseInfoForm(forms.Form):
    nickname=fields.CharField(error_messages={"required":"昵称不能为空"})
    blogUrl=fields.CharField(error_messages={"required":"昵称不能为空"})
    blogTheme=fields.IntegerField()
    blogTitle=fields.CharField(error_messages={"required":"博客标题不能为空"})

    def _clean_blogUrl(self):
        blog_obj=models.Blog.objects.filter(site=self.cleaned_data.get("blogUrl")).first()
        if blog_obj:
            return ValidationError({"message":"url地址已存在"})
        else:
            return self.cleaned_data.get("blogUrl")

class TagForm(forms.Form):

    title=fields.CharField(error_messages={"required":"标签名为空"})

class CategoryForm(forms.Form):
    title=fields.CharField(error_messages={"required":"分类名为空"})


class ArticleForm(forms.Form):

    def __init__(self,*args,**kwargs):
        super(ArticleForm,self).__init__(*args,**kwargs)
        #print(args,kwargs)
        from django.http.request import QueryDict
        if isinstance(args[0],QueryDict):
            #form默认获取的是get
            self.article_tag=args[0].getlist('article_tag')

    title=fields.CharField(error_messages={"required":"标题名为空"})
    summary=fields.CharField(error_messages={"required":"简介为空","max_length":"长度超过255个字"}
                             ,max_length=255)
    content=fields.CharField(error_messages={"required":"内容为空"})

    article_type=fields.IntegerField(error_messages={"required":"请选择文章类型"})
    article_tag=fields.CharField(error_messages={"required":"请选择标签"})
    article_category=fields.IntegerField(error_messages={"required":"请选择类别"})

    def clean_article_tag(self):
        #返回列表
        return self.article_tag








