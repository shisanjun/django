##需要实现
	仿制django admin功能
	#具体功能
	1）显示app中表对象列表（显示app名称和app中model对象）
	2）点model对象进入数据列表页
	3）数据列表页中显示choice类型和date类型数据	
	4）数据列表页过滤功能实现（保存上一次过滤的条件）
	5）数据列表页分页功能实现（首页，上一页，数字页，下一页，尾页）显示总条数
	6)动态搜索
	7）日期过滤
	8)删除
	9）action
	10）只读


	表单自定义验证
	自定义用户验证

#分页报错
加了filter之后分页报错
FieldError at /kindadmin/crm/customer
Cannot resolve keyword 'page' into field. Choices are: consult_course, consult_course_id, consultant, consultant_id, content, customerfollowup, date, enrollment, id, memo, name, payment, phone, qq, referral_from, source, tag, tag_id

一点分页，分布上面过滤的条件没有了，这是因分布A标签的原因


#from django.db.models import Q
filed.label显示的verbose内容
filed.name显示的是字段名

#实现
#复选框（多对多）

#自定仪USER AbsolutUser

customizing

还要在settings中设置
AUTH_USER_MODEL="crm.UserProfile"

#报名流程：
	1）录入客户信息
	2）销售填写报名表
		报什么班
		那个客户报

	自动生成一个链接，让学生去填写
	3）学生填写个人信息，上传身份证照片，必须点同意协议内容
	4）销售审核合同
	5）生成缴费记录
	6）账务审核
	7）状态自动改成，已报名

<pre>标签，前端输入是什么样式，后面输出就是什么样式。比合显示合同原有格式
	#是否选择
    <div class="form-group">
        <div class="col-lg-3">
            <input type="checkbox" class="form-control" id="select_contract">

        </div>
        <label class="col-lg-5">已阅读合同全部内容，并同意合同所有项</label>
    </div>
    <div class="text-center">
        <input class="btn btn-success " type="submit" value="提交" onclick="return valid_select();">
    </div>
	
	<script>
	        function valid_select(){
	            if ($("#select_contract").prop("checked")){
	                return true;
	            }
	            else {
	                alert("必须同意条款");
	                return false;
	            }
	        }
	</script>

#生成随机字符串
	方式1：
	import string
	string.ascii_lowercase
	'abcdefghijklmnopqrstuvwxyz'

	#方式2
	>>> import random
	>>> random.sample("abc",1)
	['a']
	>>> random.sample("abc",1)
	['b']
	>>> random.sample("abc",1)
	['b']
	>>> random.sample("abc",1)
	['c']


#上传图片：dropzonejs.com
	request.is_ajax()判断是不是ajax发过来的

    #如果是ajax传输过来
    if request.is_ajax():
        enroll_data_dir=os.path.join(settings.enroll_data,str(enroll_obj.id))
        if not os.path.exists(enroll_data_dir):
            os.makedirs(enroll_data_dir,exist_ok=True)#如果存在不创建

        #写入文件
        for k,file_obj in request.FILES.items():
            f=open(os.path.join(enroll_data_dir,file_obj.name),'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
        return HttpResponse("oK")



a._meta.local_many_to_many #把所有跟这个对象直接关联的m2m字段取出来
a._meta.related_objects(取所有外键）

for relate_obj in a._meta.related_objects:
	relate_obj.get_accessor_name()
make_safe

模板safe

clean
clean_name

get_or_create()获取或创建
bulk_create()批量创建


#权限管理
#url, request method,args

	学员：
		可以访问我的课程/student
		管理作业：/student/studentrecord/3
		提交作业：student/homework_detail/3

	销售：
		访问客户库/kind_admin/crm/customer


#request.auth.is_authenticated()

#把绝对的url转相对的url
	from django.core.urlresolvers import resolve
	resolve_obj=resolve(request.path)



##用户认证
	django自带用户认证系统，包括认证和授权。用户认证系统由用户，权限，用户组，密码,cookie和session给组成。
###用户认证系统设置
	#settings.py
	 INSTALLED_APPS中设置

		django.contrib.auth
		django.contrib.contenttypes
	MIDDLEWARE 中设置
		AuthenticationMiddleware 

###用户默认功能
	1）私有属性
	username
	password
	email
	first_name
	last_name

	2）创建普通用户
		from django.contrib.auth.models import User
		user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
	
	3）创建管理员
		python manage.py createsuperuser --username=joe --email=joe@example.com

	4）修改密码
		from django.contrib.auth.models import User
		u = User.objects.get(username='john')
		u.set_password('new password')
		u.save()

	5）验证用户
		from django.contrib.auth import authenticate
		user = authenticate(username='john', password='secret')
		if user is not None:
	    	#验证成功
		else:
	    	# 验证失败

	6）权限和授权
		has_add_permission() #增加权限
		has_change_permission()#修改权限
		has_delete_permission()#删除权限

		myuser.groups.set([group_list])
		myuser.groups.add(group, group, ...)
		myuser.groups.remove(group, group, ...)
		myuser.groups.clear()
		myuser.user_permissions.set([permission_list])
		myuser.user_permissions.add(permission, permission, ...)
		myuser.user_permissions.remove(permission, permission, ...)
		myuser.user_permissions.clear()

	7）默认权限在python manage.py migrate创建

	8）添加自定义权限
		比如应用名：foo 模板名： Bar
		添加: user.has_perm('foo.add_bar')
		修改: user.has_perm('foo.change_bar')
		删除: user.has_perm('foo.delete_bar')


	9)验证成功登陆
		from django.contrib.auth import authenticate, login
		
		def my_view(request):
		    username = request.POST['username']
		    password = request.POST['password']
		    user = authenticate(request, username=username, password=password)
		    if user is not None:
		        login(request, user)
		        # Redirect to a success page.
		        ...
		    else:
		        # Return an 'invalid login' error message.
		        ...

	10）检查是登陆成功（session）
		if request.user.is_authenticated:
		    # Do something for authenticated users.
		    ...
		else:
		    # Do something for anonymous users.

	11）登出
		from django.contrib.auth import logout
		def logout_view(request):
		    logout(request)		

	12）用装饰器验证是否登陆成功  
		from django.contrib.auth.decorators import login_required
		@login_required
		def my_view(request):
		
		#如果没有设置settings.LOGIN_URL，就验证没有成功，默认会跳转 
		比如 /accounts/login/?next=/polls/3/ next是你验证的页面，如果页面验证成功会还回next页面

	
		from django.contrib.auth.decorators import login_required
		#验证成功跳到指定的页面
		@login_required(login_url='/accounts/login/')
		@login_required(redirect_field_name='my_redirect_field')
		def my_view(request):


	13）限制某些用户登陆
		from django.shortcuts import redirect
		
		def my_view(request):
		    if not request.user.email.endswith('@example.com'):
		        return redirect('/login/?next=%s' % request.path)

	14）修改密码
		from django.contrib.auth import update_session_auth_hash
		
		def password_change(request):
		    if request.method == 'POST':
		        form = PasswordChangeForm(user=request.user, data=request.POST)
		        if form.is_valid():
		            form.save()
		            update_session_auth_hash(request, form.user)
		    else:
		        ...
		##
		<form method="post" action="{% url 'login' %}">
		{% csrf_token %}
		<table>
		<tr>
		    <td>{{ form.username.label_tag }}</td>
		    <td>{{ form.username }}</td>
		</tr>
		<tr>
		    <td>{{ form.password.label_tag }}</td>
		    <td>{{ form.password }}</td>
		</tr>
		</table>
		
		<input type="submit" value="login" />
		<input type="hidden" name="next" value="{{ next }}" />
		</form>

	15）默认URL
		accounts/login/ [name='login']
		accounts/logout/ [name='logout']
		accounts/password_change/ [name='password_change']
###定制用户认证

	示例：
	#在model里面写入，字段可以该成需要的
	from django.db import models
	from django.contrib.auth.models import (
	    BaseUserManager, AbstractBaseUser
	)
	
	
	class MyUserManager(BaseUserManager):
	    def create_user(self, email, date_of_birth, password=None):
	        """
	        Creates and saves a User with the given email, date of
	        birth and password.
	        """
	        if not email:
	            raise ValueError('Users must have an email address')
	
	        user = self.model(
	            email=self.normalize_email(email),
	            date_of_birth=date_of_birth,
	        )
	
	        user.set_password(password)
	        user.save(using=self._db)
	        return user
	
	    def create_superuser(self, email, date_of_birth, password):
	        """
	        Creates and saves a superuser with the given email, date of
	        birth and password.
	        """
	        user = self.create_user(
	            email,
	            password=password,
	            date_of_birth=date_of_birth,
	        )
	        user.is_admin = True
	        user.save(using=self._db)
	        return user
	
	
	class MyUser(AbstractBaseUser):
	    email = models.EmailField(
	        verbose_name='email address',
	        max_length=255,
	        unique=True,
	    )
	    date_of_birth = models.DateField()
	    is_active = models.BooleanField(default=True)
	    is_admin = models.BooleanField(default=False)
	
	    objects = MyUserManager()
	
	    USERNAME_FIELD = 'email'
	    REQUIRED_FIELDS = ['date_of_birth']
	
	    def __str__(self):
	        return self.email
	
	    def has_perm(self, perm, obj=None):
	        "Does the user have a specific permission?"
	        # Simplest possible answer: Yes, always
	        return True
	
	    def has_module_perms(self, app_label):
	        "Does the user have permissions to view the app `app_label`?"
	        # Simplest possible answer: Yes, always
	        return True
	
	    @property
	    def is_staff(self):
	        "Is the user a member of staff?"
	        # Simplest possible answer: All admins are staff
	        return self.is_admin

	#注册admin
	from django import forms
	from django.contrib import admin
	from django.contrib.auth.models import Group
	from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
	from django.contrib.auth.forms import ReadOnlyPasswordHashField
	
	from customauth.models import MyUser
	
	
	class UserCreationForm(forms.ModelForm):
	    """A form for creating new users. Includes all the required
	    fields, plus a repeated password."""
	    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
	
	    class Meta:
	        model = MyUser
	        fields = ('email', 'date_of_birth')
	
	    def clean_password2(self):
	        # Check that the two password entries match
	        password1 = self.cleaned_data.get("password1")
	        password2 = self.cleaned_data.get("password2")
	        if password1 and password2 and password1 != password2:
	            raise forms.ValidationError("Passwords don't match")
	        return password2
	
	    def save(self, commit=True):
	        # Save the provided password in hashed format
	        user = super().save(commit=False)
	        user.set_password(self.cleaned_data["password1"])
	        if commit:
	            user.save()
	        return user
	
	
	class UserChangeForm(forms.ModelForm):
	    """A form for updating users. Includes all the fields on
	    the user, but replaces the password field with admin's
	    password hash display field.
	    """
	    password = ReadOnlyPasswordHashField()
	
	    class Meta:
	        model = MyUser
	        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_admin')
	
	    def clean_password(self):
	        # Regardless of what the user provides, return the initial value.
	        # This is done here, rather than on the field, because the
	        # field does not have access to the initial value
	        return self.initial["password"]
	
	
	class UserAdmin(BaseUserAdmin):
	    # The forms to add and change user instances
	    form = UserChangeForm
	    add_form = UserCreationForm
	
	    # The fields to be used in displaying the User model.
	    # These override the definitions on the base UserAdmin
	    # that reference specific fields on auth.User.
	    list_display = ('email', 'date_of_birth', 'is_admin')
	    list_filter = ('is_admin',)
	    fieldsets = (
	        (None, {'fields': ('email', 'password')}),
	        ('Personal info', {'fields': ('date_of_birth',)}),
	        ('Permissions', {'fields': ('is_admin',)}),
	    )
	    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
	    # overrides get_fieldsets to use this attribute when creating a user.
	    add_fieldsets = (
	        (None, {
	            'classes': ('wide',),
	            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
	        ),
	    )
	    search_fields = ('email',)
	    ordering = ('email',)
	    filter_horizontal = ()
	
	# Now register the new UserAdmin...
	admin.site.register(MyUser, UserAdmin)
	# ... and, since we're not using Django's built-in permissions,
	# unregister the Group model from admin.
	admin.site.unregister(Group)


	#在setting中设置使用那个认证类
	settings.py:
	
	AUTH_USER_MODEL = 'customauth.MyUser'

##密码管理


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

#pip3豆瓣源安装

#django默认不允许外面访问，需要设置
settings.py
ALLOWED_HOSTS = ['*']

#问题1，通过subprocess连接远程主机，已经直接进入ssh环境，strace如何获取ssh进程的PID
	#在进入之前已启动个监控程序获取ssh pid 。这里也要注意，这里要过滤ssh地址，不是sshpass地址，另外可能有多个用户登陆主机，这个时候可能获取多个pid。如何获分，在登陆之前给他加个标识
	方法，ssh root@192.168.7.1 -i test （比如-i参加）
	下面在grep test

	usage: ssh [-1246AaCfghkMNnqsTtVvXxY] [-b bind_address] [-c cipher_spec]
	           [-D port] [-e escape_char] [-F configfile] [-i identity_file]
	           [-L port:host:hostport] [-l login_name] [-m mac_spec] [-o option]
	           [-p port] [-R port:host:hostport] [-S ctl] [user@]hostname [command]


#问题2： sshpass -p xxxx ssh root@192.168.1.200 登陆没有反应。
	出现这种情况是原因主机是第一个次登陆，需要authenticity
	ssh root@192.168.1.200
	The authenticity of host '192.168.1.200 (192.168.1.200)' can't be established.
	RSA key fingerprint is 9d:13:2d:ac:59:75:d9:56:7c:54:80:4a:cf:fb:a3:b1.
	Are you sure you want to continue connecting (yes/no)?
	#解决问题：
	ssh root@192.168.1.200 -o StrictHostKeyChecking=no
	Warning: Permanently added '192.168.1.200' (RSA) to the list of known hosts.
	root@192.168.1.200's password: 
#subprocess只能读取一次，再读结果为空，需要再次执行Popen
    content=subprocess.Popen("sh /home/easybastion/backend/get_ssh_pid.sh %s" %ssh_tag ,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    print(content.stdout.read(),content.stderr.read())

	是起一个独立的进程
