# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django.forms import ModelForm
from crm import models


class StudyRecordForm(ModelForm):
    def __new__(cls, *args, **kwargs):
        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs["class"] = "form-control"  # 设置样式
            # if field_name in cls.Meta.readonly_fields:
            #     field_obj.widget.attrs["disabled"]="disabled"
            # 设置长度
            # if field_name in cls.Meta.readonly_fileds:
            #     field_obj.widget.attrs["disabled"]="disabled"
        return ModelForm.__new__(cls)

    class Meta:
        model = models.StudyRecord
        fields = "__all__"
        readonly_fileds = ["student", "course_record"]


class CourseRecordForm(ModelForm):
    def __new__(cls, *args, **kwargs):

        for field_name, field_obj in cls.base_fields.items():
            field_obj.widget.attrs["class"] = "form-control"  # 设置样式
            # if field_name in cls.Meta.readonly_fields:
            #     field_obj.widget.attrs["disabled"]="disabled"
            # 设置长度
            # if field_name in cls.Meta.readonly_fileds:
            #     field_obj.widget.attrs["disabled"]="disabled"
        return ModelForm.__new__(cls)


    class Meta:
        model = models.CourseRecord
        fields = "__all__"
