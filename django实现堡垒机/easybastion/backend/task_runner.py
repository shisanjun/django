# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
import os, sys
import paramiko
import gevent
import datetime,time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


def ssh_cmd(task_detail_obj):
    """
    :paramiko实现用户执行命令
    """
    hostip=task_detail_obj.bind_host.host.ip_addr
    port=task_detail_obj.bind_host.host.port
    username=task_detail_obj.bind_host.host_user.username
    password=task_detail_obj.bind_host.host_user.password
    content=task_detail_obj.task.content

    # 实例paramiko对象
    ssh = paramiko.SSHClient()

    # 设置用户host_key自动加入
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    try:
        # 远程验证
        ssh.connect(hostname=hostip, port=port, username=username, password=password,timeout=10)
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(content)
        #获取结果
        result = stdout.read() + stderr.read()
        ssh.close()

        #更新tasklogdetail日志表
        task_detail_obj.result=result
        task_detail_obj.status=0



    except Exception as e:
        task_detail_obj.result=e
        task_detail_obj.status=1
    #task_detail_obj.end_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    task_detail_obj.save()

if __name__ == "__main__":

    #加载django环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "easybastion.settings")
    import django

    django.setup()
    from repository import models

    if len(sys.argv)<2:
        exit("请输入任务ID")
    else:
        task_id=sys.argv[1]
        task_detail_objs=models.TaskLogDetail.objects.filter(task_id=task_id).all()

        #协程列表
        gevent_list=[]
        for task_detail_obj in task_detail_objs:
            #加入协程列表
            gevent_list.append(gevent.spawn(ssh_cmd,task_detail_obj=task_detail_obj))

        #加入gevent执行
        gevent.joinall(gevent_list)