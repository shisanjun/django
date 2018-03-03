# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django.forms import ModelForm
from crm import models

class EnrollmentForm(ModelForm):

    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in  cls.base_fields.items():
            field_obj.widget.attrs["class"]="form-control" #设置样式
            #设置长度
        return ModelForm.__new__(cls)

    class Meta:
        model=models.Enrollment

        fields=["enroll_class","consultant"]



class CustomerForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in  cls.base_fields.items():

            field_obj.widget.attrs["class"]="form-control" #设置样式
            if field_name in cls.Meta.readonly_fields:
                field_obj.widget.attrs["disabled"]="disabled"
            #设置长度
        return ModelForm.__new__(cls)

    class Meta:
        model=models.Customer

        fields="__all__"
        exclude=["tag","content","memo"]
        readonly_fields=["qq","referral_from"]

class PaymentForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name,field_obj in  cls.base_fields.items():

            field_obj.widget.attrs["class"]="form-control" #设置样式
            # if field_name in cls.Meta.readonly_fields:
            #     field_obj.widget.attrs["disabled"]="disabled"
            #设置长度
        return ModelForm.__new__(cls)

    class Meta:
        model=models.PayMent
        fields="__all__"