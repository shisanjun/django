
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from django.utils.translation import ugettext_lazy as _
# Create your models here.

class IDC(models.Model):
    name=models.CharField(max_length=64,verbose_name="机房名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="机房"
        verbose_name_plural="机房"

class Host(models.Model):
    """
    主机
    """
    hostname=models.CharField(max_length=64,verbose_name="主机名")
    ip_addr=models.GenericIPAddressField(unique=True,verbose_name="主机IP")
    port=models.PositiveSmallIntegerField(default=22,verbose_name="主机断口")
    idc=models.ForeignKey("IDC",verbose_name="机房")
    enabled=models.BooleanField(default=True)

    def __str__(self):
        return self.ip_addr

    class Meta:
        verbose_name="主机信息"
        verbose_name_plural="主机信息"

class RemoteUser(models.Model):
    """
    存储远程用户名密码
    """
    username=models.CharField(max_length=64,verbose_name="主机用户")
    auth_type_choice=(
        (0,"ssh/password"),
        (1,"ssh/key")
    )

    auth_type=models.SmallIntegerField(choices=auth_type_choice,default=0,verbose_name="认证类型")

    password=models.CharField(max_length=128,blank=True,null=True,verbose_name="主机用户密码")

    def __str__(self):
        return "%s" %(self.username)

    class Meta:
        unique_together=("username","auth_type","password")
        verbose_name="主机用户"
        verbose_name_plural="主机用户"


class BindUserHosts(models.Model):
    host=models.ForeignKey(Host,verbose_name="主机")
    host_user=models.ForeignKey(RemoteUser,verbose_name="主机用户")

    def __str__(self):
        return "%s--->%s" %(self.host.ip_addr,self.host_user)

    class Meta:
        unique_together=("host","host_user")
        verbose_name="主机绑定主机用户"
        verbose_name_plural="主机绑定主机用户"



class HostGroup(models.Model):
    """
    主机组
    """
    name=models.CharField(max_length=64,unique=True,verbose_name="主机组名称")
    hosts=models.ManyToManyField(BindUserHosts,verbose_name="主机")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="主机组"
        verbose_name_plural="主机组"


class Sessions(models.Model):
    user=models.ForeignKey("UserProfile",verbose_name="系统用户")
    bind_host=models.ForeignKey("BindUserHosts",verbose_name="用户主机")
    tag=models.CharField(max_length=128,default="N/A") #uuid
    closed=models.BooleanField(default=False)
    cmd_count=models.IntegerField(default=0)#命令执行数量
    stay_time=models.IntegerField(default=0,help_text="每次刷新自动计算停留时间",verbose_name="停留时间(秒)")
    create_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s %s" %(self.user,self.bind_host)

    class Meta:
        verbose_name="审计日志"
        verbose_name_plural="审计日志"



class Tasks(models.Model):
    """
    批量任务记录表
    """
    user=models.ForeignKey("UserProfile")
    task_type_choices=(
        (0,"cmd"),
        (1,"file_transfer")
    )
    task_type=models.SmallIntegerField(choices=task_type_choices)
    content=models.TextField(verbose_name="任务内容")
    c_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)

    def __str__(self):
        return "%s %s" %(self.id,self.content)


    class Meta:
        verbose_name="操作任务"
        verbose_name_plural="操作任务"

class TaskLogDetail(models.Model):
    task=models.ForeignKey("Tasks")
    bind_host=models.ForeignKey("BindUserHosts")
    result=models.TextField()

    status_choices=(
        (0,'success'),
        (1,"failed"),
        (2,"init")
    )
    status=models.SmallIntegerField(choices=status_choices)
    c_time=models.DateTimeField(auto_now_add=True,blank=True,null=True)
    end_time=models.DateTimeField(auto_now=True,blank=True,null=True)

    def __str__(self):
        return "%s %s@%s " %(self.task.id,self.bind_host.host.ip_addr,self.bind_host.host_user.username)

    class Meta:
        verbose_name="操作任务详情"
        verbose_name_plural="操作任务详情"


class MyUserManager(BaseUserManager):
    def create_user(self, email, name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
                email=self.normalize_email(email),
                name=name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
                email,
                password=password,
                name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    """
    堡垒机账号
    """
    email = models.EmailField(
            verbose_name='邮箱地址',
            max_length=255,
            unique=True,
    )

    name = models.CharField(max_length=64, verbose_name="用户名")
    bind_host = models.ManyToManyField("BindUserHosts", verbose_name="主机", blank=True)
    bind_group = models.ManyToManyField("HostGroup", verbose_name="主机组", blank=True)
    role=models.ManyToManyField("Role",verbose_name="所属角色")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    is_admin = models.BooleanField(default=False, verbose_name="是否管理员")

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

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

    def get_short_name(self):
        return self.name

    class Meta:
        verbose_name = "系统用户"
        verbose_name_plural = "系统用户"


class Role(models.Model):
    name = models.CharField(max_length=64, verbose_name="角色名称")
    menu_one=models.ManyToManyField("MenuOne",verbose_name="一级菜单",blank=True,null=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name="角色授权"
        verbose_name_plural="角色授权"


class MenuOne(models.Model):
    name = models.CharField(max_length=64, verbose_name="一级菜单", unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="一级菜单"
        verbose_name_plural="一级菜单"

class MenuTwo(models.Model):
    name = models.CharField(max_length=64, verbose_name="二级菜单", unique=True)
    url_type_choices = (
        (0, "相对路径"),
        (1, "绝对路径"),

    )
    url_type = models.PositiveSmallIntegerField(choices=url_type_choices, default=0,verbose_name = "路径类型")
    url_path = models.CharField(max_length=128, verbose_name="路径地址")
    enable = models.BooleanField(default=True, verbose_name="是否启用菜单")
    menu_one=models.ForeignKey("MenuOne",verbose_name="上级菜单")

    def __str__(self):
        return "%s%s" %(self.name,self.url_path)

    class Meta:
        verbose_name="二级菜单"
        verbose_name_plural="二级菜单"
