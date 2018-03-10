# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
import subprocess,time
from repository import models
from django.conf import settings
class MultiTaskManage(object):

    def __init__(self,request):
        self.request=request
        self.task_id=0
        self.call_task()

    def task_parse(self):
        self.select_host_list=self.request.POST.getlist('select_host_list[]')
        self.select_host_list=list(set(self.select_host_list))
        self.exec_cmd="".join(self.request.POST.getlist('exec_cmd'))
        self.task_type=self.request.POST.get('task_type')


    def call_task(self):
        self.task_parse()

        if self.task_type=="0":#批量命令
            self.task_cmd()
        elif self.task_type=="1":#批量文件传输
            self.task_file_transfer()

    def task_cmd(self):
        """
        1.生产任务ID
        2.触发任务
        3.返回任务ID
        """

        #分配任务ID

        task_obj=models.Tasks.objects.create(user=self.request.user,task_type=self.task_type,content=self.exec_cmd)

        self.task_id=task_obj.id
        #批量初始化分配主机详情
        task_detail_list=[]
        for bind_host in self.select_host_list:
            task_detail_list.append(models.TaskLogDetail(
                task=task_obj,
                bind_host_id=bind_host,
                result="init...",#刚开始是初始化状态
                status=2,
            ))
        models.TaskLogDetail.objects.bulk_create(task_detail_list)


        #调用独立进程task_runner.py,跑任务结果（不能使用线程，主线程退出，子线程也会退出）
        subprocess.Popen("python %s %s" %(settings.CMD_EXEC_FILE,task_obj.id),shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)


    def task_file_transfer(self):
        pass

    def getTask(self):
        return self.task_id