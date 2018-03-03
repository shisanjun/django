from django.db import models
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

class HostGroup(models.Model):
    """
    主机组
    """
    name=models.CharField(max_length=64,unique=True,verbose_name="主机组名称")
    hosts=models.ManyToManyField(Host,verbose_name="主机")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="主机组"
        verbose_name_plural="主机组"



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
        return "%s(%s)" %(self.username,self.password)

    class Meta:
        unique_together=("username","auth_type","password")
        verbose_name="主机用户"
        verbose_name_plural="主机用户"


class BindHosts(models.Model):
    host=models.ForeignKey(Host,verbose_name="主机")
    host_user=models.ForeignKey(RemoteUser,verbose_name="主机用户")

    class Meta:
        unique_together=("host","host_user")


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

    name = models.CharField(max_length=64,verbose_name="用户名")
    bind_host=models.ManyToManyField("Host",verbose_name="主机",blank=True)
    bind_group=models.ManyToManyField("HostGroup",verbose_name="主机组",blank=True)
    is_active = models.BooleanField(default=True,verbose_name="是否激活")
    is_admin = models.BooleanField(default=False,verbose_name="是否管理员")

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
        verbose_name="系统用户"
        verbose_name_plural="系统用户"