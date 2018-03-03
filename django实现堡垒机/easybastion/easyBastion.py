# _*_ coding:utf-8 _*_
__author__ = "shisanjun"

import os

if __name__=="__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "easybastion.settings")
    import django
    django.setup()

    from backend.main import HostManage
    host_manage=HostManage()
    host_manage.interactive()