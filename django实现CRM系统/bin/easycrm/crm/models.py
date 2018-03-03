from django.db import models
from django.contrib.auth.models import User,PermissionsMixin
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Customer(models.Model):
    """
    客户信息表
    """
    name=models.CharField(max_length=32,blank=True,null=True,verbose_name="姓名")#blank 是django admin允许为空;blank=True,null=True成对出现
    qq=models.CharField(max_length=64,unique=True,verbose_name="QQ")
    phone=models.CharField(max_length=64,blank=True,null=True,verbose_name="电话")
    source_choice=(
        (1,"转介绍"),
        (2,"QQ群"),
        (3,"官网"),
        (4,"百度推广"),
        (5,"51cto"),
        (6,"知呼"),
        (7,"市场推广"),
    )
    source=models.SmallIntegerField(choices=source_choice,verbose_name="推广渠道")
    referral_from=models.CharField(verbose_name="转介绍人qq",max_length=64,blank=True,null=True)
    consult_course=models.ForeignKey("Course",verbose_name="咨询课程")
    content=models.TextField(verbose_name="咨询详情")
    consultant=models.ForeignKey("UserProfile",verbose_name="客服")
    memo=models.TextField(blank=True,null=True,verbose_name="备注")
    tag=models.ManyToManyField("Tag",verbose_name="标签")
    status_choice=(
        (0,"未报名"),
        (1,"已所名"),
    )
    status=models.SmallIntegerField(verbose_name="报名状态",choices=status_choice,default=0)
    date=models.DateTimeField(auto_now_add=True,verbose_name="时间")

    def __str__(self):
        return self.qq

    class Meta:
        verbose_name="客户信息"
        verbose_name_plural="客户信息"

class Tag(models.Model):
    """
    标签
    """
    name=models.CharField(max_length=64,unique=True,verbose_name="标签名称")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="标签信息"
        verbose_name_plural="标签信息"

class CustomerFollowUp(models.Model):
    """
    客户跟进表
    """
    customer=models.ForeignKey("Customer",verbose_name="客户")
    content=models.TextField(verbose_name="跟进内容")
    consultant=models.ForeignKey("UserProfile",verbose_name="客服")
    date=models.DateTimeField(auto_now_add=True,verbose_name="时间")
    intention_choices=(
        (0,"2周内报名"),
        (1,"1个月内报名"),
        (2,"近期无报名计划"),
        (3,"已在其他机构报名"),
        (4,"已报名"),
        (5,"已拉黑"),
    )

    intention=models.SmallIntegerField(choices=intention_choices,verbose_name="报名意向")

    def __str__(self):
        return "<%s:%s>" %(self.customer.qq,self.intention)

    class Meta:
        verbose_name="客户跟进"
        verbose_name_plural="客户跟进"


class Course(models.Model):
    """
    课程表
    """
    name=models.CharField(max_length=64,unique=True,verbose_name="课程名称")
    price=models.PositiveSmallIntegerField(default=0,verbose_name="课程价格")
    period=models.PositiveSmallIntegerField(verbose_name="周期(月)")
    outline=models.TextField(verbose_name="课程大纲")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name="课程信息"
        verbose_name_plural="课程信息"

class Branch(models.Model):
    """
    分校
    """
    name=models.CharField(max_length=128,unique=True,verbose_name="分校名称")
    addr=models.CharField(max_length=128,verbose_name="分校地址")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name="分校信息"
        verbose_name_plural="分校信息"


class Contract(models.Model):
    """
    合同
    """
    name=models.CharField(max_length=64,verbose_name="合同名称")
    content=models.TextField(verbose_name="全同内容")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural="合同管理"
        verbose_name="合同管理  "

class ClassList(models.Model):
    """
    班级表
    """
    barach=models.ForeignKey("Branch",verbose_name="校区")
    course=models.ForeignKey("Course",verbose_name="课程")
    contract=models.ForeignKey("Contract",verbose_name="合同",blank=True,null=True)
    class_type_choices=(
        (0,"面授(脱产)"),
        (1,"面授(周末)"),
        (2,"网络班"),
    )
    semester=models.PositiveSmallIntegerField(verbose_name="学期")
    terchers=models.ManyToManyField("UserProfile",verbose_name="讲师")
    start_date=models.DateField(verbose_name="开班日期")
    end_date=models.DateField(verbose_name="结业日期",blank=True,null=True)

    def __str__(self):
        return "%s校区 %s课程 第%s期" %(self.barach,self.course,self.semester)

    class Meta:
        unique_together=("barach","course","semester")
        verbose_name="班级信息"
        verbose_name_plural="班级信息"

class CourseRecord(models.Model):
    """
    上课记录
    """
    from_class=models.ForeignKey("ClassList",verbose_name="班级")
    day_num=models.PositiveSmallIntegerField(verbose_name="第几节(天)")
    teacher=models.ForeignKey("UserProfile",verbose_name="讲师")
    has_homework=models.BooleanField(default=True,verbose_name="是否有作业")
    homework_title=models.CharField(max_length=128,blank=True,null=True,verbose_name="作业标题")
    homework_content=models.TextField(blank=True,null=True,verbose_name="作业内容")
    outline=models.TextField(verbose_name="本节课程大纲")

    def __str__(self):
        return ("%s %s") %(self.from_class,self.day_num)

    class Meta:
        unique_together=("from_class","day_num")
        verbose_name="上课记录"
        verbose_name_plural="上课记录"


class StudyRecord(models.Model):
    """
    学习记录
    """
    student=models.ForeignKey("Enrollment",verbose_name="报名表")
    course_record=models.ForeignKey("CourseRecord",verbose_name="上课记录")
    attendence_choice=(
        (0,'已签到'),
        (1,'迟到'),
        (2,'缺勤'),
        (3,'早退'),
    )
    attendence=models.SmallIntegerField(choices=attendence_choice,default=0,verbose_name="上课状态")
    score_choices=(
        (100,'A+'),
        (90,'A'),
        (85,'B+'),
        (80,'B'),
        (75,'C+'),
        (65,'C'),
        (40,'C-'),
        (-50,'D'),
        (-100,'COPY'),
        (0,'N/A'),
    )
    score=models.SmallIntegerField(choices=score_choices,verbose_name="成绩")
    memo=models.TextField(blank=True,null=True,verbose_name="成绩")
    date=models.DateField(auto_now_add=True,verbose_name="日期")
    def __str__(self):
        return "%s %s %s" %(self.student,self.course_record,self.score)

    class Meta:
        verbose_name="学习记录"
        verbose_name_plural="学习记录"
        unique_together=("student","course_record")

class Enrollment(models.Model):
    """
    报名表
    """
    customer=models.ForeignKey("Customer",verbose_name="客户")
    enroll_class=models.ForeignKey("ClassList",verbose_name="所报班级")
    consultant=models.ForeignKey("UserProfile",verbose_name="课程顾问")
    contract_agreed=models.BooleanField(default=False,verbose_name="学员已同意合同")
    contract_approved=models.BooleanField(default=False,verbose_name="合同已审核")
    date=models.DateTimeField(auto_now_add=True,verbose_name="日期")

    def __str__(self):
        return "%s %s" %(self.customer,self.enroll_class)

    class Meta:
        unique_together=("customer","enroll_class")
        verbose_name="报名信息"
        verbose_name_plural="报名信息"

class PayMent(models.Model):
    """
    支付表
    """
    customer=models.ForeignKey("Customer",related_name="payment" ,related_query_name="payment",verbose_name="客户")
    course=models.ForeignKey("Course",verbose_name="所报课程")
    amount=models.PositiveIntegerField(verbose_name="数额",default=500)
    consultant=models.ForeignKey("UserProfile",verbose_name="客服")

    date=models.DateTimeField(auto_now_add=True,verbose_name="日期")

    class Meta:
        verbose_name="付款信息"
        verbose_name_plural="付款信息"





class Role(models.Model):
    """
    角色表
    """
    name=models.CharField(max_length=32,unique=True,verbose_name="角色名称")
    menus=models.ManyToManyField("Menu",related_query_name="menus",related_name="menus",verbose_name="拥有功能")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name="角色信息"
        verbose_name_plural="角色信息"

class Menu(models.Model):
    """
    菜单表
    """
    name=models.CharField(max_length=32,unique=True,verbose_name="菜单名称") #菜单名称
    url_name=models.CharField(max_length=64,verbose_name="相对或者绝对URL")          #urls中的name

    url_type_choices=(
        (0,"alias"),
        (1,"absolute_url"),
    )
    url_type=models.SmallIntegerField(choices=url_type_choices,default=0,verbose_name="相对还是绝对URL")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name="菜单信息"
        verbose_name_plural="菜单信息"


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
        # user.is_superuser=True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='用户邮箱',
        max_length=255,
        unique=True,
        help_text="请输入用户邮箱"
    )
    name = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(_('password'), max_length=128,help_text="<a href='password.html'>修改密码</a>")
    roles=models.ManyToManyField("Role",blank=True,verbose_name="所在角色")
    is_active = models.BooleanField(default=True,verbose_name="是否激活")
    is_admin = models.BooleanField(default=False,verbose_name="是否管理员")
    stu_account=models.ForeignKey("Customer",verbose_name="关联客户",blank=True,null=True)
    objects = MyUserManager()

    USERNAME_FIELD = 'email'#那个字段做用户名
    REQUIRED_FIELDS = ['name']#那些字段是必须的

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

    @property #判断是不是一个员工
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    class Meta:
        verbose_name_plural="用户信息"
        verbose_name="用户信息"
        permissions=(
            ("can_access_my_course","可以访问我的课程"),
            ("can_access_customer","可以访问客户"),
            ('can_access_customer_detail','用户详情'),
            ('can_access_homework','学员作业情况'),
            ('can_access_homework_detail','查看作业'),
            ('can_port_homework_detail',"提交作业"),
        )