# _*_ coding:utf-8 _*_
__author__ = "shisanjun"
from crm import models
from django.shortcuts import HttpResponse,render,redirect
from django.utils.translation import gettext as _
enabled_admin={}
class BaseAdmin(object):
    list_display=[]
    list_filter=[]
    list_per_page=20
    search_fields=[]
    orderby=None
    filter_horizontal=[]
    exclude_field=[]
    readonly_fields=[]
    readonly_table=False

    actions=["delete_selected_objs",]

    def delete_selected_objs(self,request,querysets):
        print("delete_selected_objs",self,request,querysets)

        table_name=self.model._meta.model_name
        app_name=self.model._meta.app_label
        select_ids=",".join([str(i.id) for i in querysets])
        errors={}
        if self.readonly_table:
            errors = {"readonly_table": "The Table is Readonly!"}
        if request.POST.get("delete_confirm")=="yes":
            querysets.delete()
            return redirect("/kindadmin/%s/%s" %(app_name,table_name))
        return render(request, "kindadmin/table_delete.html", {"objs": querysets,
                                                                   "admin": self,
                                                                   "app_name": app_name,
                                                                   "table_name": table_name,
                                                                    "errors":"",
                                                                    "select_ids":select_ids,
                                                                    "action":request._admin_action,
                                                                    "errors":errors
                                                               })

    def default_form_validation(self):
        print("default_form_validation",self)

class CustomerAdmin(BaseAdmin):
    list_display=["id","qq","phone","name",'consultant',"source","status","date","enroll"]
    list_filter = ["source","consultant","tag","date"]
    search_fields = ("name","qq",)
    orderby = ["id",]
    filter_horizontal=["tag",]
    readonly_fields=["qq","name","consultant","tag"]
    readonly_table=True

    def enroll(self):
        if self.instance.status==1:
            link_name="报名新课程"
        else:
            link_name="报名"
        return "<a href='/crm/customer/%s/enroll/'>%s</a>" %(self.instance.id,link_name) #传递ID呈
    enroll.display_name="报名链接"


    def default_form_validation(self):
        consult_content=self.cleaned_data.get("content")
        if len(consult_content)<15:
            return  self.ValidationError(
                    _(" Field %(field)s 咨询内容记录不能少于15个"),
                   code="invalid",
                   params={'field':"content"},
               )

    def clean_phone(self):
        print("chean_phone:",self.cleaned_data.get("phone"))
        if not self.cleaned_data.get("phone"):
          self.add_error("phone","must phone")
        return self.cleaned_data.get("phone")


class CustomerFollowUpAdmin(BaseAdmin):
    list_display=["content",]

class UserprofileAdmin(BaseAdmin):
    list_display=["email","name","is_admin","is_active","stu_account"]
    exclude_field=["last_login","groups","user_permissions","superuser_status"]


class CourseRecordAdmin(BaseAdmin):
    list_display = ["from_class","day_num","teacher","has_homework","homework_title"]

    actions = ("initCourseRecord",)

    def initCourseRecord(self,request,queryset):
        # print("初始化上课记录")
        # print(queryset[0].from_class.enrollment_set.all())


        bulk_objs=[]
        for enroll_obj in queryset[0].from_class.enrollment_set.all():
            # models.StudyRecord.objects.get_or_create(
            #     student=enroll_obj,
            #     course_record=queryset[0],
            #     attendence=0,
            #     score=0,
            # )
            bulk_objs.append(models.StudyRecord(
                student=enroll_obj,
                course_record=queryset[0],
                attendence=0,
                score=0,
            ))
        try:
            models.StudyRecord.objects.bulk_create(bulk_objs)#批量创建，要么成功，要么出错
        except:
            return HttpResponse("批量初始化学习记录失败，请检查该节课是否已有对应的学习记录")
        return redirect("/kindadmin/crm/studyrecord?course_record=%s" %queryset[0].id)
    initCourseRecord.short_description = "初始化上课记录"


class StudentRecordAdmin(BaseAdmin):
    list_display = ("student","course_record","attendence","score","date")
    list_filter = ("student","course_record","score","attendence")

class TagsAdmin(BaseAdmin):
    list_display = ("name",)

class CustomerFollowUpAdmin(BaseAdmin):
    list_display = ("customer","consultant","intention","date")


class CourseAdmin(BaseAdmin):
    list_display = ("name","price","period")


class BranchAdmin(BaseAdmin):
    list_display = ("name","addr")

class ContractAdmin(BaseAdmin):
    list_display = ("name",)


class ClassListAdmin(BaseAdmin):
    list_display = ("barach","course","contract","semester","terchers",'start_date',"end_date")


class EnrollmentAdmin(BaseAdmin):
    list_display = ("customer","enroll_class","consultant","contract_agreed","contract_approved","date")

class PayMentAdmin(BaseAdmin):
    list_display = ("customer","course","amount","consultant","date")

class RoleAdmin(BaseAdmin):
    list_display = ("name",)
    filter_horizontal=["menus",]
class MenuAdmin(BaseAdmin):
    list_display = ("name","url_name")


def register(model_class,admin_class):
    #通过model名子，去找app名子
    #model_class._meta.app_label    通过model，去找app名字
    #model_class._meta.model_name   通过model，去找表的名字
    if model_class._meta.app_label not in enabled_admin:
        enabled_admin[model_class._meta.app_label ]={}
    admin_class.model=model_class #admin_class加属性
    enabled_admin[model_class._meta.app_label ][model_class._meta.model_name]=admin_class

register(models.Customer,CustomerAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.UserProfile,UserprofileAdmin)
register(models.CourseRecord,CourseRecordAdmin)
register(models.StudyRecord,StudentRecordAdmin)
register(models.UserProfile,UserprofileAdmin)
register(models.Tag,TagsAdmin)
register(models.CustomerFollowUp,CustomerFollowUpAdmin)
register(models.Course,CourseAdmin)
register(models.Branch,BranchAdmin)
register(models.Contract,ContractAdmin)
register(models.ClassList,ClassListAdmin)
register(models.Enrollment,EnrollmentAdmin)
register(models.PayMent,PayMentAdmin)
register(models.Role,RoleAdmin)
register(models.Menu,MenuAdmin)