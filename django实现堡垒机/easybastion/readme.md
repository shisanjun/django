配置django环境
	自己写的程序想加载django环境
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "easybastion.settings") #环境加入系统
    import django
    django.setup() #加载所有app

	from backend import main #导入自己的模块


#strace抓取远程操作命令

strace -fp 15712 -t -o strace.log

#自动输入密码sshpass
sshpass -p 123456 ssh root@192.168.1.1


#subprocess 不能使用Popen方法会退出
	使用run方法，退出可以正常回到ptyhon下面


#依赖包
sshpass
paramiko
theadpool
gevent并发使用协程

from concurrent.futures import ThreadPoolExecute

#JS变量不能传递给模板变量,要当作参数传递
比如：
function GetTaskResult(task_id){
$.getJson("{%url 'task_reslut' %}",{"task_id":task_id},funcion(callback){
 }
})
}