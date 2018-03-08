# -*- coding:utf-8 -*-
__author__ = 'shisanjun'
from repository import  models
class MakeSession(object):
    """
    每次远程登陆生成一个会话
    """


    def session(self,user,bind_host,tag):
        session_obj=models.Sessions.objects.create(user=user,bind_host=bind_host,tag=tag)

        return session_obj.id
