
###主机管理

####要求：
	通过前端页面实现操作后台数据库：实现增删改查
	实现主机分组
	实现不同的用户可以管理不同的主机
	在前端可以对主机信息实现增删改查

####博客地址:
	http://www.cnblogs.com/lixiang1013/category/1103148.html


##程序结构
	├── hostmanage
	│   ├── db.sqlite3					#数据库
	│   ├── hostmanage
	│   │   ├── __init__.py
	│   │   ├── settings.py				#设置文件
	│   │   ├── urls.py					#url
	│   │   └── wsgi.py
	│   ├── machine						#主机管理app
	│   │   ├── admin.py
	│   │   ├── apps.py
	│   │   ├── __init__.py
	│   │   ├── migrations
	│   │   ├── models.py
	│   │   ├── tests.py
	│   │   ├── urls.py
	│   │   └── views.py
	│   ├── manage.py
	│   ├── static						#静态文件目录	
	│   │   ├── bootstrap-3.3.7-dist
	│   │   ├── css
	│   │   │   ├── common.css
	│   │   │   └── other.css
	│   │   ├── img
	│   │   └── js
	│   │       ├── hostmanage.js
	│   │       └── jquery-1.12.4.js
	│   └── templates					#模板目录
	│       ├── host2user.html			#主机和用户关联模板
	│       ├── host_add.html			#主机添加模板
	│       ├── host_delete.html			#主机删除模板
	│       ├── host_edit.html			#主机编辑模板
	│       ├── hostgroup.html			#主机组管理
	│       ├── host.html				#主机管理
	│       ├── index.html				#首页
	│       ├── left.html				#左边导航菜单
	│       ├── login.html				#登陆页面
	│       ├── muban.html				#母板
	│       ├── top.html					#头部导航
	│       ├── usergroup.html			#用户组管理
	│       └── user.html				#用户管理



###1. 程序说明
	通过前端页面实现操作后台数据库：实现增删改查
	实现主机分组
	实现不同的用户可以管理不同的主机
	在前端可以对主机信息实现增删改查

###2. 测试用例

        账号1：root 密码:1234


###3. 程序测试
	python python培训作业/DAY17-李祥-django主机管理/bin/hostmanage/manage.py runserver 8000

###4. 测试
	1）首页：http://127.0.0.1:8000

	2）用户登陆：http://127.0.0.1:8000/login
		cookie实现1天，7天，一个月免登陆

	3）用户退出

	4）主机管理：http://127.0.0.1:8000/machine/host/
		a)主机列表信息：序号，主机名，主机IP，主机端口，主机机柜，创建时间，主机配置，主机组
		b)主机添加：http://127.0.0.1:8000/machine/host_add 
		c)编辑：http://127.0.0.1:8000/machine/host_edit-5（主机序号）跳转到编辑页面
		d)删除:http://127.0.0.1:8000/machine/host_delete-6（主机序号）跳转到删除页面

	5) 主机组管理：http://127.0.0.1:8000/machine/hostgroup/

		a)主机组信息：序号，主机组名称
		b)主机组添加：模态对话框和ajax实现主机组添加
		b)主机组编辑：模态对话框和ajax实现主机组编辑
		b)主机组删除：ajax实现主机组删除

	6) 用户管理：http://127.0.0.1:8000/machine/user/

		a)用户信息：序号，id，用户名，用户密码，用户组，主机管理
		b)用户添加：模态对话框和ajax实现用户添加
		b)用户编辑：模态对话框和ajax实现用户编辑
		b)用户删除：ajax实现用户删除

	7) 用户组管理：http://127.0.0.1:8000/machine/usergroup/

		a)用户组信息：序号，ID	，用户角色名
		b)用户组添加：模态对话框和ajax实现用户组添加
		b)用户组编辑：模态对话框和ajax实现用户组编辑
		b)用户组删除：ajax实现用户组删除

	8) 用户申请管理主机：http://127.0.0.1:8000/machine/userhost
