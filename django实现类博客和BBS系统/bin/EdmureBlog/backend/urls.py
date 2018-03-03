from django.conf.urls import url
from django.conf.urls import include
from .views import user

urlpatterns = [
    url(r'^base-info.html$', user.base_info,name="base_info"),
    url(r'^avatar-img.html$', user.avatar_img,name="avatar_img"),
    url(r'^tag.html$', user.tag,name="tag"),
    url(r'^tag_del.html$', user.tag_del,name="tag_del"),
    url(r'^tag_edit.html$', user.tag_edit,name="tag_edit"),
    url(r'^category.html$', user.category,name="category"),
    url(r'^category_del.html$', user.category_del,name="category_del"),
    url(r'^category_edit.html$', user.category_edit,name="category_edit"),
    url(r'^article.html$', user.article,name="article"),
    url(r'^article-del.html$', user.article_del,name="article_del"),
    url(r'^add-article.html$', user.add_article,name="add_article"),
    url(r'^edit-article-(?P<nid>\d+).html$', user.edit_article,name="edit_article"),
    url(r'^condition-(?P<article_type>\d+)-(?P<category_id>\d+)-(?P<tags_id>\d+).html$', user.condtion_article,name="condtion_article"),
]
