开发一个简单的BBS论坛

####要求：
	需求：
	1、整体参考“抽屉新热榜” ＋ “虎嗅网”
	2、实现不同论坛版块
	3、帖子列表展示
	4、帖子评论数、点赞数展示
	5、在线用户展示
	6、允许登录用户发贴、评论、点赞
	7、允许上传文件
	8、帖子可被置顶
	9、可进行多级评论

####博客地址:
	http://www.cnblogs.com/lixiang1013/category/1103148.html


##程序结构
	EdmureBlog                  #bbs+博客
    ├── backend
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── __init__.py
    │   ├── migrations
    │   ├── models.py
    │   ├── tests.py
    │   ├── urls.py
    │   └── views
    │       └── user.py
    ├── blog.sqlite3          #数据库
    ├── EdmureBlog				
    │   ├── __init__.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── manage.py
    ├── repository           #数据仓库
    │   ├── admin.py
    │   ├── apps.py
    │   ├── __init__.py
    │   ├── migrations
    │   │   ├── __init__.py
    │   ├── models.py
    │   ├── templatetags
    │   │   ├── __init__.py
    │   │   └── simple_filter.py
    │   └── tests.py
    ├── static           #静态文件目录
    │   ├── css
    │   ├── imgs
    │   ├── js
    │   ├── plugins
    │   └── upload
    ├── templates       #静态模板
    │   ├── backend_add_article.html   #文章添加
    │   ├── backend_article.html		   #文章管理
    │   ├── backend_base_info.html	   #基础信息
    │   ├── backend_category.html	   #分类管理
    │   ├── backend_edit_article.html  #文章编辑
    │   ├── backend_layout.html		   #后台母模板
    │   ├── backend_tag.html			   #标签管理
    │   ├── home_detail.html			   #博客详情
    │   ├── home.html    			   #博客首页       
    │   ├── home_layout.html			   #博客母模板
    │   ├── home_summary_list.html     #分类过滤
    │   ├── home_title_list.html		   #博客文章列表
    │   ├── include
    │   │   ├── header.html			   #首页头部
    │   │   └── menu.html			   #菜单
    │   ├── index.html				   #首页
    │   ├── login.html				   #登陆
    │   ├── register_1.html
    │   └── register.html              #注册
    ├── utils						   #工具
    │   ├── authication.py			   #认证
    │   ├── check_code.py			   #验证码
    │   ├── pagination.py              #分页
    └── web							   #前端
        ├── admin.py
        ├── apps.py
        ├── forms.py
        ├── __init__.py
        ├── migrations
        │   └── __init__.py
        ├── models.py
        ├── tests.py
        ├── urls.py
        └── views
            ├── account.py
            ├── home1.py
            ├── home.py



###1. 程序说明
	1、整体参考“抽屉新热榜” ＋ “虎嗅网”
	2、实现不同论坛版块
	3、帖子列表展示
	4、帖子评论数、点赞数展示
	5、在线用户展示
	6、允许登录用户发贴、评论、点赞
	7、允许上传文件
	8、帖子可被置顶
	9、可进行多级评论

###2. 测试用例

        账号1：test1 密码：123456

###3. 程序测试
	初始化数据库：
		python manage.py makemigrations  
		python manage.py migrate   
	运行程序：
		python培训作业/DAY18-李祥-博客/bin/EdmureBlog/manage.py runserver 127.0.0.1:8000
	           

###4. 测试
	1）首页：http://127.0.0.1:8000/
		1.过滤python,linux,openstack,golang
		2.查看阅读最多的文章
		3.查看评论最多的文章
		4.个人博客，管理中心，注销

	2）注册页面：http://127.0.0.1:8000/register.html
		1.用户名不能为空,用户名已存在
		2.邮箱不通为空，验证邮箱格式，邮件已存在
		3.密码不能为空

		注册成功跳转到后台页面，是否开开通博客。

	3）用户登陆：http://127.0.0.1:8000/login.html
		1.用户名不能为空，验证用户存不存在
		2.密码不能为空
		3.验证码不能为空
		4.用户名或者密码不正确

		登陆成功跳转到首页
	4) 管理中心：http://127.0.0.1:8000/backend/base-info.html
	
	5）个人信息：http://127.0.0.1:8000/backend/base-info.html

	6）标签管理：http://127.0.0.1:8000/backend/tag.html
		1.ajax实现添加，删除，编辑

	7）分类管理：http://127.0.0.1:8000/backend/category.html
		1.ajax实现添加，删除，编辑

	8）文章管理：http://127.0.0.1:8000/backend/article.html
		1.新url方式实现添加和编辑
		2.按类型，分类，标签快速过滤

	9）博客首页：http://127.0.0.1:8000/test1.html
		1）个人信息
		2）标签，分类，时间统计和过滤
		3）文章列表
		4）添加关注
	10）文章：http://127.0.0.1:8000/test1/5.html
		1）赞和踩
		2）多级评论
		


