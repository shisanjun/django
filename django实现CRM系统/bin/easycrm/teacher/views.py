from django.shortcuts import render,redirect,HttpResponse
from django.http import FileResponse
from django.urls import reverse
from crm import models
from teacher import forms
from easycrm import settings

import os
import json
# Create your views here.
def teacher_index(request):

    return render(request,"teacher/teacher_index.html")


def teacher_course(request,class_id):
    course_record_objs=models.CourseRecord.objects.filter(from_class_id=class_id,teacher=request.user).all()


    return render(request,"teacher/teacher_course.html",
                  {
                      "course_record_objs":course_record_objs,
                      "class_id":class_id
                  })


def teacher_study(request,course_id):
    course_obj=models.CourseRecord.objects.get(id=course_id)
    study_objs=models.StudyRecord.objects.filter(course_record_id=course_id).all()
    attendence_choice=models.StudyRecord.attendence_choice
    score_choicese=models.StudyRecord.score_choices
    ret={"status":False,"error":None}
    if request.method=="POST":
        ids=request.POST.getlist("ids")
        for id_tmp in ids:
            id_tmp=json.loads(id_tmp)
            id=id_tmp.get("id")
            attendence=id_tmp.get("attendence")
            score=id_tmp.get("score")
            study_obj=models.StudyRecord.objects.filter(id=id).update(attendence=attendence,score=score)

        ret["status"]=True
        return HttpResponse(json.dumps(ret))

    return  render(request,"teacher/teacher_study.html",
                   {"study_objs":study_objs,
                    "course_obj":course_obj,
                    "attendence_choice":attendence_choice,
                    "score_choicese":score_choicese,
                    "course_id":course_id
                    })

def teacher_homework_detail(request,study_id):
    """
    审批作业
    :param request:
    :param study_id:
    :return:
    """
    study_obj=models.StudyRecord.objects.get(id=study_id)
    class_id=str(study_obj.student.enroll_class.id)
    course_id=str(study_obj.course_record.from_class.course.id)
    courserecord_id=str(study_obj.course_record.id)
    customer_id=str(study_obj.student.customer.id)
    file_dict={}
    if request.method=="GET":
        study_form=forms.StudyRecordForm(instance=study_obj)

        #班级/课程/上课记录/学员号

        file_dir="{class_id}/{course_id}/{courserecord_id}/{customer_id}".format(

            class_id=class_id,
            course_id=course_id,
            courserecord_id=courserecord_id,
            customer_id=customer_id,
        )
        path_dir=os.path.join(settings.homework_data,file_dir)
        try:
            for file_name in os.listdir(path_dir):
                file_dict[file_name]=[class_id,course_id,courserecord_id,customer_id,file_name]
        except:
            pass

    elif request.method=="POST":
        study_post_copy=request.POST.copy()
        study_post_copy["student"]=study_obj.student.id
        study_post_copy["course_record"]=study_obj.course_record.id

        study_form=forms.StudyRecordForm(study_post_copy,instance=study_obj)

        if study_form.is_valid():
            study_form.save()
            return redirect(reverse("teacher_study",args=(course_id,)))

    return render(request,"teacher/teacher_homework_detail.html",
              {"study_form":study_form,
               "study_obj":study_obj,
              "file_dict":file_dict})

def homework_down(request,class_id,course_id,courserecord_id,customer_id,filename):
    """
    下载文件

    :param request:
    :param class_id:
    :param course_id:
    :param courserecord_id:
    :param customer_id:
    :param filename:
    :return:
    """
    file_path_name="{class_id}/{course_id}/{courserecord_id}/{customer_id}/{file_name}".format(

        class_id=class_id,
        course_id=course_id,
        courserecord_id=courserecord_id,
        customer_id=customer_id,
        file_name=filename
    )

    abs_file_name=os.path.join(settings.homework_data,file_path_name)
    f=open(abs_file_name,"rb")
    response=FileResponse(f)
    response["Content-Type"]="applicaion/octet-stream"
    response["Content-Disposition"]='attachment;filename="%s"' %filename
    return response


def teacher_courserecord_add(request,class_id):
    """
    增加上课记录
    :param request:
    :param class_id:
    :return:
    """
    classes_obj=models.ClassList.objects.get(id=class_id)

    if request.method=="GET":

        course_record_form=forms.CourseRecordForm()

    elif request.method=="POST":
        data_copy=request.POST.copy()
        data_copy["from_class"]=classes_obj.id
        data_copy["teacher"]=request.user.id

        print(data_copy)
        course_record_form=forms.CourseRecordForm(data_copy)
        if course_record_form.is_valid():
            course_record_form.save()
            return redirect(reverse("teacher_course",args=(class_id,)))
        print(course_record_form.errors)
    return render(request,"teacher/teacher_courserecord.html",
                      {"classes_obj":classes_obj,
                       "course_record_form":course_record_form
                       })


def init_studyecord(request):
    """
    批量初始化上课记录
    :param request:
    :return:
    """
    ret={"status":False,"data":None,"error":None}
    if request.method=="POST":

        course_record_ids=request.POST.getlist("course_record_ids")
        bulk_objs=[]
        for course_record_id in course_record_ids:
            course_record_obj=models.CourseRecord.objects.get(id=course_record_id)
            for enroll_obj in course_record_obj.from_class.enrollment_set.all():

                bulk_objs.append(models.StudyRecord(
                    student=enroll_obj,
                    course_record_id=course_record_id,
                    attendence=0,
                    score=0,
                ))

        try:
            models.StudyRecord.objects.bulk_create(bulk_objs)#批量创建，要么成功，要么出错
            ret["status"]=True
            ret["data"]="批量初始化学习记录成功"
        except:
            ret["error"]="批量初始化学习记录失败，请检查该节课是否已有对应的学习记录"
        return HttpResponse(json.dumps(ret))
