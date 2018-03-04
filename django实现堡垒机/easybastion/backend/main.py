# _*_ coding:utf-8 _*_
__author__ = "shisanjun"

from django.contrib.auth import authenticate
import subprocess
import uuid
class HostManage(object):

    def interactive(self):
        print("login to bastion".center(50,"-"))
        count=0
        #登陆验证
        while count<3:

            username=input("input username:")
            password=input("input password:")
            self.user=authenticate(username=username,password=password)

            if not self.user: #验证不成功
                count+=1
                if count<3:
                    print("用户名或者密码不正确")
                else:
                    exit("用户登陆密码超过3次不正确，程序将退出")
            else:
                print("welcome  %s".center(50,"-") %self.user)
                break

        #进入主机组选择
        while True:

            for index,host_group in enumerate(self.user.bind_group.all()): #select_related
                print("%s.\t%s[%s]" %(index,host_group.name,host_group.hosts.all().count()))

            print("z.\t未分组主机[%s]" %(self.user.bind_host.all().count()))

            choice=input("请选择主机组序号,q退出选择>>")
            if len(choice)==0:continue
            if choice=='q':break
            if str(choice).isdigit():
                choice_int=int(choice)
                if choice_int>=0 and choice_int<=index:
                    select_host_group=self.user.bind_group.all()[choice_int].hosts.all()
                    self.select_host_func(select_host_group)

            #未分配主机
            if choice=="z":
                select_host_group=self.user.bind_host.all()
                self.select_host_func(select_host_group)

    def select_host_func(self,select_host_group):
        #进入主机选择
        while True:
            for index,bind_host in enumerate(select_host_group):
                print("%s.\t%s" %(index,bind_host))

            choice=input("请选择主机序号,q退出选择>>")
            if len(choice)==0:continue
            if choice=='q':break
            if str(choice).isdigit():
                choice_int=int(choice)
                if choice_int>=0 and choice_int<=index:
                    bind_host=select_host_group[choice_int]
                    print("login into host:  [%s]" %(bind_host.host))
                    #生成需要监控的ssh的uuid
                    ssh_tag=uuid.uuid4()

                    #在登陆主机前监控到主机登陆后的pid
                    content=subprocess.Popen("sh /home/easybastion/backend/get_ssh_pid.sh %s" %ssh_tag ,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
                    #print(content.stdout.read(),content.stderr.read())

                    #获取主机IP，主机用户和密码
                    host_ip=bind_host.host.ip_addr
                    host_type=bind_host.host_user.auth_type

                    host_username=bind_host.host_user.username
                    host_password=bind_host.host_user.password

                    if host_type==0: #0 代表密码登陆验证

                        ssh_login_str="sshpass -p {host_password} ssh {host_username}@{host_ip} -i {ssh_tag} -o StrictHostKeyChecking=no".format(
                            host_password=host_password,
                            host_username=host_username,
                            host_ip=host_ip,
                            ssh_tag=ssh_tag
                        )
                        #登陆到主机,Popen相当于打开一个文件，操作和退出会不正常
                        subprocess.run(ssh_login_str,shell=True)

                    elif host_type==1:#1 代表秘钥免密码登陆
                        subprocess.run("ssh %s" %host_ip,shell=True)

