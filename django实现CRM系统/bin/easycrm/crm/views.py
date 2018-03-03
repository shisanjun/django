from django.shortcuts import render,HttpResponse,redirect
from crm import forms
from crm import models
from easycrm import settings
import os
from django.db.models.deletion import    IntegrityError
# Create your views here.

def enrollment(request,nid):

    customer_obj=models.Customer.objects.filter(id=nid).first()

    link_url={}
    if request.method=="GET":

        form_obj=forms.EnrollmentForm()
        return render(request,"sales/enrollment.html",{"form_obj":form_obj,"customer_obj":customer_obj})
    elif request.method=="POST":
        form_obj=forms.EnrollmentForm(request.POST)
        if form_obj.is_valid():
            try:
                form_obj.cleaned_data["customer"]=customer_obj
                enroll_obj=models.Enrollment.objects.create(**form_obj.cleaned_data)
                enroll_obj.save()
                link_url["info"]="请将此链接发送给客户:http://localhost:8000/crm/customer/registion/%s/"%enroll_obj.id
            except IntegrityError as e:

                enroll_obj=models.Enrollment.objects.get(customer_id=nid,enroll_class_id=form_obj.cleaned_data[
                                                         "enroll_class"].id)

                if enroll_obj.contract_agreed:

                    return redirect("/crm/customer/contract_review/%s" %enroll_obj.id)
                else:
                    form_obj.add_error("__all__", "该用户词条报名信息已经存在,不能重复创建")
                    link_url["info"]="请将此链接发送给客户:http://localhost:8000/crm/customer/registion/%s/"%enroll_obj.id
        return render(request,"sales/enrollment.html",{"form_obj":form_obj,"customer_obj":customer_obj,'link_url':link_url})

def registion(request,nid):

    customer_obj=models.Customer.objects.filter(id=nid).first()
    enroll_obj=models.Enrollment.objects.filter(customer_id=nid).first()
    status=0

    if request.method=="GET":
        form_obj=forms.CustomerForm(instance=customer_obj)

    elif request.method=="POST":
        #如果是ajax传输过来
        if request.is_ajax():
            enroll_data_dir=os.path.join(settings.enroll_data,str(enroll_obj.id))
            if not os.path.exists(enroll_data_dir):
                os.makedirs(enroll_data_dir,exist_ok=True)#如果存在不创建

            #写入文件
            for k,file_obj in request.FILES.items():
                f=open(os.path.join(enroll_data_dir,file_obj.name),'wb')
                for chunk in file_obj.chunks():
                    f.write(chunk)
            return HttpResponse("oK")

        form_obj=forms.CustomerForm(request.POST,instance=customer_obj)
        if form_obj.is_valid():

            customer_obj.save()
            enroll_obj.contract_agreed=True
            enroll_obj.save()
            status=1
            return render(request, "sales/registion.html", {"status": status})
        else:

            if enroll_obj.contract_agreed == True:
                status = 1
            else:
                status = 0
            form_obj = forms.CustomerForm(instance=enroll_obj.customer)

    return render(request,"sales/registion.html",{"form_obj":form_obj,
                                                  "enroll_obj":enroll_obj,
                                                  "status":status
                                                  })

def contract_review(request,enroll_id):
    enroll_obj = models.Enrollment.objects.filter(id=enroll_id).first()
    enroll_form_obj=forms.EnrollmentForm(instance=enroll_obj)
    customer_form = forms.CustomerForm(instance=enroll_obj.customer)
    return render(request, "sales/contract_review.html",
                  {"enroll_form_obj": enroll_form_obj,
                  "customer_form":customer_form,
                  "enroll_obj":enroll_obj})

def enroll_rejection(request,enroll_id):

    if request.method=="GET":
        enroll_obj=models.Enrollment.objects.filter(id=enroll_id).first()
        enroll_obj.contract_agreed=False
        enroll_obj.save()
        return redirect("/crm/customer/%s/enroll/" %enroll_obj.customer.id)


def payment(request,enroll_id):
    enroll_obj = models.Enrollment.objects.filter(id=enroll_id).first()
    errors=[]


    if request.method=="POST":

        amount=request.POST.get("amount",0)

        if len(amount)!=0:
            if int(amount)<500:
                errors.append("学费金额至少500元")
            else:
                payment_obj=models.PayMent.objects.create(
                    customer_id=enroll_obj.customer.id,
                    course_id=enroll_obj.enroll_class.course.id,
                    amount=amount,
                    consultant_id=enroll_obj.consultant.id
                )
                #学习已同意合同
                enroll_obj.contract_agreed=True
                enroll_obj.save()

                #修改学员报名状态
                enroll_obj.customer.status=1
                enroll_obj.customer.save()

                return redirect("/kindadmin/crm/customer")

        else:
            errors.append("学费金额至少500元")

    return render(request, "sales/payment.html",
                  { "enroll_obj":enroll_obj,
                    "errors":errors
                    })