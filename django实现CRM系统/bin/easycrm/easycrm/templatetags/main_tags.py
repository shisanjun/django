# _*_ coding:utf-8 _*_
__author__ = "shisanjun"

from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse
register = template.Library()


@register.simple_tag
def display_menus(user):
    """
    显示菜单
    :param user:
    :return:
    """
    roles=user.roles.all()
    menu_list=[]
    menu_str='<ul class="sub-menu-list">'
    for role in roles:
        for menu in role.menus.all():
            if menu not in menu_list:
                menu_list.append(menu.name)
                if menu.url_type ==0:
                    menu_str+='<li><a href="'+reverse(menu.url_name)+'"> '+menu.name+'</a></li>'
                else:
                    menu_str+='<li><a href="'+ menu.url_name + '"> '+ menu.name+'</a></li>'
            else:
                continue

    menu_str+='</ul>'
    return mark_safe(menu_str)
