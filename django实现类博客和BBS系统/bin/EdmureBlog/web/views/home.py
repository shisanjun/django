#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect
from repository import models
from utils.authication import login
from utils import pagination
from django.urls import reverse
import json
from django.db.models import Max,Count
from collections import Counter

def index(request):
    """
    博客首页，展示全部博文
    :param request:
    :return:
    """
    type=request.GET.get("type","0")
    if type=="0":
        article_lists = models.Article.objects.all().order_by("-nid")
    else:
        article_lists = models.Article.objects.filter(article_type=type).order_by("-nid")
    current_page = request.GET.get('p', 1)
    current_page = int(current_page)
    val = request.COOKIES.get('per_page_count',10)
    val = int(val)
    page_obj = pagination.Page(current_page=current_page,data_count=len(article_lists),per_page_count=val)
    data = article_lists[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(reverse("index"))
    article_type=models.Article.type_choices

    read_count_objs=models.Article.objects.values("nid","read_count","title").annotate(read_count_max=Max("read_count")).order_by("-read_count_max")[:7]
    commnet_count_objs=models.Article.objects.values("nid","comment_count","title").annotate(comment_count_max=Max("comment_count")).order_by("-comment_count_max")[:7]

    return render(request, 'index.html', {'article_lists': data,
                                          "page_str":page_str,
                                          "article_type":article_type,
                                          "read_count_objs":read_count_objs,
                                          "commnet_count_objs":commnet_count_objs,
                                          })


def month_group():
    #按年月分组
    article_objs2=models.Article.objects.annotate(num_comment=Count("nid")).filter(create_time__isnull=False).order_by("-num_comment")
    year_month_list=[(p.create_time.year,p.create_time.month) for p in article_objs2]
    year_month_dict=Counter(year_month_list)

    date_list=[(key[0],key[1],year_month_dict[key]) for key in year_month_dict]
    date_list.sort(reverse=True)
    return date_list


def menu(site):

    blog_home = models.Blog.objects.filter(site=site).select_related('user').first()
    fans_count=models.UserFans.objects.filter(user_id=blog_home.user.nid).count()
    relate_fans_count=models.UserFans.objects.filter(follower_id=blog_home.user.nid).count()
    category_objs=models.Category.objects.filter(blog_id=blog_home.nid)
    tag_objs=models.Tag.objects.filter(blog_id=blog_home.nid)
    article_objs=models.Article.objects.filter(blog_id=blog_home.nid).order_by("-nid")
    month_objs=month_group
    return {
        "blog_home":blog_home,
        "fans_count":fans_count,
        "relate_fans_count":relate_fans_count,
        "category_objs":category_objs,
        "tag_objs":tag_objs,
        "article_objs":article_objs,
        "month_objs":month_objs,
        "site":site
    }

@login
def home(request,site):
    """
    博主个人首页
    :param request:
    :param site: 博主的网站后缀如：http://xxx.com/wupeiqi.html
    :return:
    """

    render_objs=menu(site)
    blog_home=render_objs.get("blog_home")
    article_objs=models.Article.objects.filter(blog_id=blog_home.nid).order_by("-nid")
    render_objs["article_objs"]=article_objs

    return render(request, 'home.html',render_objs )


def filter(request, site, condition, val):
    """
    分类显示
    :param request:
    :param site:
    :param condition:
    :param val:
    :return:
    """
    user_home = models.Blog.objects.filter(site=site).select_related('user').first()
    if not user_home:
        return redirect('/')

    template_name = "home_summary_list.html"
    if condition == 'tag':
        # print("tag")
        template_name = "home_summary_list.html"
        article_list = models.Article.objects.filter(tags__nid=val, blog=user_home).all()
        # print(article_list)
    elif condition == 'category':
        template_name = "home_summary_list.html"
        article_list = models.Article.objects.filter(category__nid=val, blog=user_home).all()
    elif condition == 'date':
        template_name = "home_summary_list.html"
        article_list = models.Article.objects.filter(blog=user_home).extra(
            where=['date_format(create_time,"%%Y%%m")=%s'], params=[val, ]).all()
    else:
        article_list = []

    menu_dict=menu(site)
    menu_dict["article_list"]=article_list
    return render(request, template_name,menu_dict)


def detail(request, site, nid):
    """
    博文详细页
    :param request:
    :param site:
    :param nid:
    :return:
    """

    render_dict=menu(site)
    blog_home=render_dict.get("blog_home")

    article_obj=models.Article.objects.filter(blog_id=blog_home.nid,nid=nid).first()
    #阅读加1
    article_obj.read_count=int(article_obj.read_count)+1
    article_obj.save()

    comment_objs=models.Comment.objects.filter(article_id=nid)

    render_dict["article_obj"]=article_obj
    render_dict["comment_objs"]=comment_objs

    return render(request, 'home_detail.html',render_dict)

def up_article(request):

    res={"status":False,"data":None}
    if request.method=="GET":
        username=request.GET.get("site")
        article_id=request.GET.get("nid")
        user_obj=models.UserInfo.objects.filter(username=username).first()
        article_obj=models.Article.objects.filter(nid=article_id).first()
        updown_obj=models.UpDown.objects.filter(article_id=article_id,user_id=user_obj.nid).first()

        #不存在
        if  updown_obj is None:
            models.UpDown.objects.create(article_id=article_id,user_id=user_obj.nid,up=True)
            #文章踩加1
            article_obj.up_count+=1
            article_obj.save()
            res["status"]=True
        #赞存在
        else:
            #是赞还是踩
            if not updown_obj.up:#不是赞
                #踩改成赞
                updown_obj.up=True
                updown_obj.save()

                article_obj.up_count+=1
                article_obj.down_count-=1
                article_obj.save()
                res["status"]=True

    return HttpResponse(json.dumps(res))

def down_article(request):

    res={"status":False,"data":None}
    if request.method=="GET":
        username=request.GET.get("site")
        article_id=request.GET.get("nid")
        user_obj=models.UserInfo.objects.filter(username=username).first()
        article_obj=models.Article.objects.filter(nid=article_id).first()
        updown_obj=models.UpDown.objects.filter(article_id=article_id,user_id=user_obj.nid).first()
        #赞不存在
        if  updown_obj is None:
            models.UpDown.objects.create(article_id=article_id,user_id=user_obj.nid,up=False)
            #文章踩加1
            article_obj.down_count+=1
            article_obj.save()

            res["status"]=True
        #赞存在
        else:
            #是赞还是踩
            if  updown_obj.up: #是赞
                #赞改成踩
                updown_obj.up=False
                updown_obj.save()

                article_obj.down_count+=1
                article_obj.up_count-=1
                article_obj.save()
                res["status"]=True

    return HttpResponse(json.dumps(res))


def replay_article(request):
    """
    评论文章
    :param request:
    :return:
    """
    # print(request.POST)
    ret={"status":False,"data":None,"error":None}
    if request.method=="POST":
        article_id=request.POST.get("article_id")
        content=request.POST.get("content")
        username=request.POST.get("username")
        user_obj=models.UserInfo.objects.filter(username=username).first()
        try:
            comment_obj=models.Comment.objects.create(content=content,article_id=article_id,user_id=user_obj.nid)
            article_obj=models.Article.objects.filter(nid=article_id).first()
            #评论加1
            article_obj.comment_count+=1
            article_obj.save()
            ret["status"]=True
        except:
            ret["status"]=False
            ret["error"]="创建失败"
        return HttpResponse(json.dumps(ret))


def fans_add(request):
    """
    添加关注
    :param request:
    :return:
    """
    ret={"status":False,"data":None,"error":None}
    if request.method=="GET":
        site=request.GET.get("site")
        username=request.GET.get("username")
        if site==username:

            ret["error"]="用户不能添加自己为粉丝"
        else:
            site_obj=models.UserInfo.objects.filter(username=site).first()
            fan_user_obj=models.UserInfo.objects.filter(username=username).first()
            try:
                fan_obj=models.UserFans.objects.create(user_id=site_obj.nid,follower_id=fan_user_obj.nid)
                ret["status"]=True
                ret["data"]="关注成功，您已是[%s]的粉丝"%site
            except:
                ret["error"]="已是[%s]的粉丝" %site

    return HttpResponse(json.dumps(ret))

def fans_cancel(request):
    """
    取消关注
    :param request:
    :return:
    """
    ret={"status":False,"data":None,"error":None}
    if request.method=="GET":
        site=request.GET.get("site")
        username=request.GET.get("username")
        if site==username:

            ret["error"]="用户不能添加或者取消自己为粉丝"
        else:
            site_obj=models.UserInfo.objects.filter(username=site).first()
            fan_user_obj=models.UserInfo.objects.filter(username=username).first()

            fan_obj=models.UserFans.objects.filter(user_id=site_obj.nid,follower_id=fan_user_obj.nid)
            if fan_obj is not None:
                fan_obj.delete()
                ret["status"]=True
                ret["data"]="已取消为[%s]的粉丝"%site


    return HttpResponse(json.dumps(ret))

def show_article(request,article_id):
    """
    查看文章
    :param request:
    :param article_id:
    :return:
    """
    if request.method=="GET":
        article_obj=models.Article.objects.filter(nid=article_id).first()
        return redirect("/%s/%s.html" %(article_obj.blog.site,article_id))

def replay_otheruser(request):
    """
    回复其他人
    :param request:
    :return:
    """
    ret={"status":False,"data":None,"error":None}
    if request.method=="POST":
        comment_id=request.POST.get("comment_id")
        replay_comment=request.POST.get("replay_comment")
        article_id=request.POST.get("article_id")
        username=request.POST.get("username")
        user_obj=models.UserInfo.objects.filter(username=username).first()
        comment_user=request.POST.get("comment_user")
        comment_obj=models.Comment.objects.create(
            reply_id=comment_id,
            content=replay_comment,
            article_id=article_id,
            user_id=user_obj.nid
        )
        if comment_obj is not None:
            ret["status"]=True

    return HttpResponse(json.dumps(ret))

