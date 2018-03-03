from django.shortcuts import render,HttpResponse
from crm import models
from easycrm import settings
import os
import time
import json
from crm.permissions import permission
# Create your views here.




@permission.check_permission
def student_index(request):

    return render(request,"student/student_index.html")

@permission.check_permission
def homework(request,enroll_id):
    enroll_obj=models.Enrollment.objects.get(id=enroll_id)
    if request.method=="GET":
        course_record_objs=models.CourseRecord.objects.filter(from_class=enroll_obj.enroll_class)
    return  render(request,'student/homework.html',{"course_record_objs":course_record_objs,
                                                        "enroll_obj":enroll_obj
                                                    })
@permission.check_permission
def homework_detail(request,courserecord_id):
    course_record_obj=models.CourseRecord.objects.get(id=courserecord_id)
    customer_id=request.user.stu_account.id
    print(customer_id)
    ret={"status":False,"data":None,"error":None,"file_lists":None}
    file_dir="{class_id}/{course_id}/{courserecord_id}/{customer_id}".format(
        class_id=course_record_obj.from_class.id,
        course_id=course_record_obj.from_class.course.id,
        courserecord_id=course_record_obj.id,
        customer_id=customer_id,
    )
    path_dir=os.path.join(settings.homework_data,file_dir)


    if request.method=="POST":
        if not os.path.isdir(path_dir):
            os.makedirs(path_dir,exist_ok=True)

        for k,file_obj in request.FILES.items():
            with open(os.path.join(path_dir,file_obj.name),"wb") as f:
                for chunk in file_obj.chunks(): #一点点写数据
                    f.write(chunk)


    file_lists=[]
    try:
        for file_name in os.listdir(path_dir):
            f_path=os.path.join(path_dir,file_name)
            modify_time=time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(os.stat(f_path).st_mtime))
            file_lists.append([file_name,os.stat(f_path).st_size,modify_time])
    except:
        pass

    ret["file_lists"]=file_lists

    if request.method=="POST":
        return HttpResponse(json.dumps(ret))


    return render(request,"student/homework_detail.html",
                  {"course_record_obj":course_record_obj
                   })