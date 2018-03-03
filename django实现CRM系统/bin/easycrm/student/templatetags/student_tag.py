# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from django import template
from django.db.models import Sum
from crm import models
register=template.Library()

@register.simple_tag
def display_sum_score(enroll_obj):

    studyrecord_obj= models.StudyRecord.objects.filter(student_id=enroll_obj.id).aggregate(sum_score=Sum("score"))
    if studyrecord_obj is not None:

        return studyrecord_obj
    else:
        return 0

@register.simple_tag
def  display_courserecord_score(enroll_obj,course_record_obj):
    return models.StudyRecord.objects.filter(student=enroll_obj,course_record=course_record_obj).values("score").first()