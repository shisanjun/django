# _*_ coding:utf-8 _*_
__author__ = "shisanjun"

from django.contrib.auth import authenticate


class HostManage(object):

    def interactive(self):
        print("-------run-----")
        username=input("请输入堡垒机用户名:")
        password=input("请输入堡垒机用户密码:")
        user=authenticate(username=username,password=password)
        print(user)
        if user:
            print(user.bind_group)
            for host in user.bind_group.all():
                print(host)
        else:
            print("用户名或者密码不正确")
