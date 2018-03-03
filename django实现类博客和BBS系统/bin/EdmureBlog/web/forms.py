from django import forms
from django.forms import fields
from django.forms import widgets
from repository import models
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = fields.CharField(error_messages={"required": "用户名不能为空"})
    password = fields.CharField(error_messages={"required": "密码不能为空"})
    check_code = fields.CharField(error_messages={"required": "验证码不能为空"})
    cookietime = fields.BooleanField(required=False)

    def clean_username(self):
        """
        验证用户存不存在
        :return:
        """
        obj = models.UserInfo.objects.filter(username=self.cleaned_data['username'])
        # 用户存在返回原来的值
        if obj:
            return self.cleaned_data['username']
        else:
            raise ValidationError(message="用户不存在", code="xxxx")

    def clean(self):
        """
        验证用户名和密码存不存在
        :return:
        """
        obj = models.UserInfo.objects.filter(username=self.cleaned_data.get("username"),
                                             password=self.cleaned_data.get("password"))
        if obj:
            return self.cleaned_data
        else:
            raise ValidationError(message="用户名或者密码不正确")


class RegisterForm(forms.Form):
    username = fields.CharField(
            error_messages={"required": "用户名不能为空"},
            widget=widgets.Input(attrs={"class": "form-control"})
    )
    email = fields.EmailField(
           error_messages={'required':'邮箱不能为空','invalid':'邮箱格式错误'},
            widget=widgets.Input(attrs={"class": "form-control"})
    )
    password = fields.CharField(
            error_messages={"required": "密码不能为空"},
            widget=widgets.Input(attrs={"class": "form-control"})
    )
    password2 = fields.CharField(error_messages={"required": "密码不能为空"},
                                 widget=widgets.Input(attrs={"class": "form-control"}))
    check_code = fields.CharField(error_messages={"required": "验证码不能为空"},
                                  widget=widgets.Input(attrs={"class": "form-control"}))

    def clean_username(self):
        """
        验证用户存不存在
        :return:
        """
        obj = models.UserInfo.objects.filter(username=self.cleaned_data['username'])
        # 用户存在返回原来的值
        if not obj:
            return self.cleaned_data['username']
        else:
            raise ValidationError(message="用户已存在，请更换其他用户名", code="xxxx")


    def clean_email(self):
        """
        验证用户存不存在
        :return:
        """
        obj = models.UserInfo.objects.filter(username=self.cleaned_data['email'])
        # 用户存在返回原来的值
        if not obj:
            return self.cleaned_data['email']
        else:
            raise ValidationError(message="邮件已存在，请更换其他邮箱", code="xxxx")