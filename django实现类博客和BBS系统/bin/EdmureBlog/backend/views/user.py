#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,redirect,HttpResponse
from repository import models
from backend import forms
from django.core.exceptions import ValidationError
from django.urls import reverse
from utils import pagination
from utils.authication import auth,login
import json
import os



class JsonCunstomEncode(json.JSONEncoder):
    """
    #ErrorDict类型数据转字典
    """
    def default(self, field):
        if isinstance(field,ValidationError):
            return {"code":field.code,"message":field.message}
        else:
            return json.JSONEncoder.default(self,field)


@login
def base_info(request):
    """
    博主个人信息
    :param request:
    :return:
    """

    if request.method=="GET":
        username=request.session.get("username")
        user_obj=models.UserInfo.objects.filter(username=username).first()
        blog_obj=models.Blog.objects.filter(user_id=user_obj.nid).first()
        theme_obj=models.Theme.objects.all()

        return render(request, 'backend_base_info.html',{"user_obj":user_obj,"blog_obj":blog_obj,"theme_obj":theme_obj})
    elif request.method=="POST":
        username=request.session.get("username")
        user_obj=models.UserInfo.objects.filter(username=username).first()
        ret={"status":False,"error":None,"data":None}
        obj=forms.BaseInfoForm(request.POST)
        if obj.is_valid():

            nickname=obj.cleaned_data.get("nickname")
            blog_title=obj.cleaned_data.get("blogTitle")
            blog_theme=obj.cleaned_data.get("blogTheme")
            blog_url=obj.cleaned_data.get("blogUrl")
            models.UserInfo.objects.filter(username=username).update(nickname=nickname)
            blog_obj=models.Blog.objects.filter(site=blog_url).first()
            if not blog_obj:
                blog_obj=models.Blog.objects.create(title=blog_title,site=blog_url,theme_id=blog_theme,user_id=user_obj.nid)
                request.session["blog_id"]=blog_obj.nid
            else:
                blog_obj=models.Blog.objects.filter(nid=blog_obj.nid).update(title=blog_title,site=blog_url,theme_id=blog_theme)
                request.session["blog_id"]=blog_obj

            ret["status"]=True

        else:
            ret["error"]=obj.errors.as_json()
        result=json.dumps(ret)
        return HttpResponse(result)


from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def avatar_img(request):
    ret={"status":False,'data':None}
    if request.method=="POST":
        #获取文件
        file_obj=request.FILES.get("file_obj")
        #获取文件名
        filename=file_obj.name
        img_path=os.path.join("static/upload/",filename)
        with open(img_path,'wb') as f:
            #一点点写文件
            for line in file_obj.chunks():
                f.write(line)
        ret["status"]=True
        ret["data"]=img_path
        username=request.session.get("username")
        user_obj=models.UserInfo.objects.filter(username=username).update(avatar="/%s" %img_path)

    return HttpResponse(json.dumps(ret))

@auth
def tag(request):
    """
    博主个人标签管理
    :param request:
    :return:
    """
    if request.method=="GET":

        tag_objs=models.Tag.objects.filter(blog_id=request.session.get("blog_id")).select_related()
        #分页
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        val = request.COOKIES.get('per_page_count',10)
        val = int(val)
        page_obj = pagination.Page(current_page=current_page,data_count=len(tag_objs),per_page_count=val)
        data = tag_objs[page_obj.start:page_obj.end]
        page_str = page_obj.page_str(reverse("tag"))

        return render(request, 'backend_tag.html',{"tag_objs":data,"page_str":page_str})

    elif request.method=="POST":
        tag_fm=forms.TagForm(request.POST)

        if tag_fm.is_valid():

            tag_obj=models.Tag.objects.filter(title=tag_fm.cleaned_data["title"],blog_id=request.session.get("blog_id")).first()
            if tag_obj:
                 return render(request,"backend_tag.html",{"error":"此用户下标签已存在"})
            else:
                models.Tag.objects.create(title=tag_fm.cleaned_data["title"],blog_id=request.session.get("blog_id"))
                return redirect(reverse("tag"))
        else:
            return render(request,"backend_tag.html",{"tag_fm":tag_fm})

@auth
def tag_del(request):
    """
    删除标签
    """
    ret={"status":False,"data":None}
    if request.method=="POST":

        nid=request.POST.get("nid")
        tag_obj=models.Tag.objects.filter(nid=nid).delete()
        if tag_obj:
            ret["status"]=True
        return HttpResponse(json.dumps(ret))


@auth
def tag_edit(request):
    ret={'status':False}
    if request.method=="POST":
        nid=request.POST.get("nid")
        title=request.POST.get("title")
        tag_obj=models.Tag.objects.filter(nid=nid).update(title=title)
        if tag_obj:
            ret["status"]=True
        return HttpResponse(json.dumps(ret))

@auth
def category(request):
    """
    博主个人分类管理
    :param request:
    :return:
    """
    if request.method=="GET":
        category_objs=models.Category.objects.filter(blog_id=request.session.get("blog_id")).select_related()
                #分页
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        val = request.COOKIES.get('per_page_count',10)
        val = int(val)
        page_obj = pagination.Page(current_page=current_page,data_count=len(category_objs),per_page_count=val)
        data = category_objs[page_obj.start:page_obj.end]
        page_str = page_obj.page_str(reverse("tag"))
        return render(request, 'backend_category.html',{"category_objs":data,"page_str":page_str})

    elif request.method=="POST":

        category_fm=forms.CategoryForm(request.POST)

        if category_fm.is_valid():

            tag_obj=models.Category.objects.filter(title=category_fm.cleaned_data["title"],blog_id=request.session.get("blog_id")).first()
            if tag_obj:
                 return render(request,"backend_category.html",{"error":"此用户下分类已存在"})
            else:
                models.Category.objects.create(title=category_fm.cleaned_data["title"],blog_id=request.session.get("blog_id"))
                return redirect(reverse("category"))
        else:
            return render(request,"backend_category.html",{"category_fm":category_fm})
    return render(request, 'backend_category.html')


@auth
def category_del(request):
    """
    删除分类
    :param request:
    :param nid:
    :return:
    """
    ret={"staus":False,"data":None}
    if request.method=="POST":
        nid=request.POST.get("nid")
        category_obj=models.Category.objects.filter(nid=nid).delete()
        if category_obj:
            ret["status"]=True
        return HttpResponse(json.dumps(ret))

@auth
def category_edit(request):
    ret={'status':False}
    if request.method=="POST":
        nid=request.POST.get("nid")
        title=request.POST.get("title")
      #  print(request.POST)
        tag_obj=models.Category.objects.filter(nid=nid).update(title=title)
        if tag_obj:
            ret["status"]=True
        return HttpResponse(json.dumps(ret))

@auth
def article(request):
    """
    博主个人文章管理
    :param request:
    :return:
    """

    if request.method=="GET":
        article_objs=models.Article.objects.filter(blog_id=request.session.get("blog_id")).order_by("-nid")
                #分页
        current_page = request.GET.get('p', 1)
        current_page = int(current_page)
        val = request.COOKIES.get('per_page_count',10)
        val = int(val)
        page_obj = pagination.Page(current_page=current_page,data_count=len(article_objs),per_page_count=val)
        data = article_objs[page_obj.start:page_obj.end]
        page_str = page_obj.page_str(reverse("article"))
        article_type_objs=models.Article.type_choices
        tag_objs=models.Tag.objects.filter(blog_id=request.session.get("blog_id"))
        category_objs=models.Category.objects.filter(blog_id=request.session.get("blog_id"))
        article_dict={
        "article_type":0,
        "category_id":0,
        "tags_id":0
    }
        return render(request, 'backend_article.html',
                      {"article_objs":data,
                       "page_str":page_str,
                       "tag_objs":tag_objs,
                       "category_objs":category_objs,
                       "article_type_objs":article_type_objs,
                       "article_dict":article_dict,
                       })

@auth
def condtion_article(request,*args,**kwargs):


    tags_id=kwargs.get("tags_id",0)
    article_type=kwargs.get("article_type",0)
    category_id=kwargs.get("category_id",0)

    article_dict={}
    if article_type!="0":
        article_dict["article_type"]=article_type
    if category_id!="0":
        article_dict["category_id"]=category_id
    if tags_id!="0":
        tag_objs=models.Tag.objects.filter(nid=tags_id).first()
        article_dict["tags"]=tag_objs

    article_objs=models.Article.objects.filter(**article_dict)
    # print(kwargs)
    # print(article_dict)
    #分页
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    val = request.COOKIES.get('per_page_count',10)
    val = int(val)
    page_obj = pagination.Page(current_page=current_page,data_count=len(article_objs),per_page_count=val)
    data = article_objs[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(reverse("tag"))

    article_type_objs=models.Article.type_choices
    tag_objs=models.Tag.objects.filter(blog_id=request.session.get("blog_id"))
    category_objs=models.Category.objects.filter(blog_id=request.session.get("blog_id"))

    return render(request, 'backend_article.html',
                  {"article_objs":data,
                   "page_str":page_str,
                   "tag_objs":tag_objs,
                   "category_objs":category_objs,
                   "article_type_objs":article_type_objs,
                   "article_dict":kwargs,
                   })

@auth
def add_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    ret={"status":False,"data":None,"error":None}
    if request.method=="GET":

        tag_objs=models.Tag.objects.filter(blog_id=request.session.get("blog_id")).select_related()
        category_objs=models.Category.objects.filter(blog_id=request.session.get("blog_id")).select_related()
        return render(request, 'backend_add_article.html',{"tag_objs":tag_objs,"category_objs":category_objs})
    elif request.method=="POST":

        article_fm=forms.ArticleForm(request.POST)
        if article_fm.is_valid():

            ret["status"]=True
            # print(article_fm.cleaned_data.get("article_category"))
            article_obj=models.Article.objects.create(
                    title=article_fm.cleaned_data.get("title"),
                    summary=article_fm.cleaned_data.get("summary"),
                    blog_id=request.session.get("blog_id"),
                    category_id=article_fm.cleaned_data.get("article_category"),
                    article_type=article_fm.cleaned_data.get("article_type"),
            )

            for article_tag_id in article_fm.cleaned_data.get("article_tag"):
                models.Article2Tag.objects.create(article_id=article_obj.nid,tag_id=article_tag_id)

            models.ArticleDetail.objects.create(content=article_fm.cleaned_data.get("content"),article_id=article_obj.nid)


        else:
            ret["error"]=article_fm.errors.as_json()
        return HttpResponse(json.dumps(ret))

@auth
def article_del(request):
    """
    删除文章
    :param request:
    :return:
    """
    ret={"status":False}
    if request.method=="POST":
        nid=request.POST.get("nid")
        article_obj=models.Article.objects.filter(nid=nid).delete()
        if article_obj:
            ret["status"]=True
        return HttpResponse(json.dumps(ret))

@auth
def edit_article(request,nid):
    """
    编辑文章
    :param request:
    :return:
    """

    if request.method=="GET":
        article_obj=models.Article.objects.filter(nid=nid).first()
        article_type_objs=models.Article.type_choices

        category_objs=models.Category.objects.filter(blog_id=request.session.get("blog_id"))
        tag_objs=models.Tag.objects.filter(blog_id=request.session.get("blog_id"))
        return render(request, 'backend_edit_article.html',
                      {"article_obj":article_obj,
                       "article_type_objs":article_type_objs,
                       "category_objs":category_objs,
                       "tag_objs":tag_objs
                       })

    elif request.method=="POST":

        article_fm=forms.ArticleForm(request.POST)
        if article_fm.is_valid():
            title=article_fm.cleaned_data.get("title")
            summary=article_fm.cleaned_data.get("summary")
            content=article_fm.cleaned_data.get("content")
            article_type=article_fm.cleaned_data.get("article_type")
            article_tag=article_fm.cleaned_data.get("article_tag")

            article_category=article_fm.cleaned_data.get("article_category")

            models.Article.objects.filter(nid=nid).update(title=title,
                                                                      summary=summary,
                                                                      category_id=article_category,
                                                                      article_type=article_type)

            article_obj=models.Article.objects.filter(nid=nid).first()

            for article_tag_id in article_tag:

                article_tag_obj=models.Article2Tag.objects.filter(article_id=article_obj.nid,tag_id=article_tag_id).count()

                if not article_tag_obj:
                    article_tag_obj=models.Article2Tag.objects.create(article_id=article_obj.nid,tag_id=article_tag_id)

            models.ArticleDetail.objects.filter(article_id=article_obj.nid).update(content=content)
        return redirect(reverse("article"))