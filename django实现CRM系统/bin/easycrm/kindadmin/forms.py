# _*_ coding:utf-8 _*_
__author__ = "shisanjun"

from django.forms import fields,ModelForm,ValidationError
from crm import models
from django.utils.translation import gettext as _
class CustomeerModelForm(ModelForm):
    class Meta:
        model=models.Customer
        fields="__all__"


#需要动态生成表单,ModelForm是类，类是由type()生成的，可以用type动态生成类
def create_model_form(request,admin_class):

    #加样式modelForm默认没有样式，通过new方法加上样式。cls.base_fields是所有字段的字典
    def __new__(cls,*args,**kwargs):
        for field_name,field_obj in  cls.base_fields.items():
            field_obj.widget.attrs["class"]="form-control" #设置样式
            #设置长度
            field_obj.widget.attrs["maxlength"]= getattr(field_obj,"max_length") if hasattr(field_obj,"max_length") \
                else ""


            #判断是增加还是修改
            #print(hasattr(admin_class,"is_add_form"))
            if not hasattr(admin_class,"is_add_form"):
                #判断只读
                if field_name in admin_class.readonly_fields:
                    field_obj.widget.attrs["disabled"]='disabled'

            #表单验证
            if hasattr(admin_class, "clean_%s" % ( field_name )):
                field_clean_func = getattr(admin_class, "clean_%s" %( field_name))
                setattr(cls, "clean_%s" % (field_name), field_clean_func)

        return ModelForm.__new__(cls)


    def default_clean(self):
        """给所有的form默认加一个clean验证"""
        error_lists=[]


        #通过判断obj.instance是增加还是修改，
        if self.instance:#表示是修改，如果是增加不需要做只读验证
            for field in admin_class.readonly_fields:
                field_val = getattr(self.instance, field) #val in db
                if hasattr(field_val, "select_related"):
                    m2m_objs = getattr(field_val, "select_related")().select_related()
                    m2m_vals = [i[0] for i in m2m_objs.values_list("id")]
                    set_m2m_vals = set(m2m_vals)
                    set_m2m_vals_from_fronted = set([i.id for i in self.cleaned_data.get(field)])
                    if set_m2m_vals != set_m2m_vals_from_fronted:
                        error_lists.append(ValidationError(
                            _('Field %(value)s is Readonly'),
                            code='invalid',
                            params={'value': field},
                        ))
                    continue

                field_val_from_fronted=self.cleaned_data.get(field)

                if   field_val!= field_val_from_fronted:
                   error_lists.append( ValidationError(
                       _(" Field %(field)s is readonly data should be %(val)s"),
                       code="invalid",
                       params={'field':field,"val":field_val},
                   ))
        if error_lists:
            raise ValidationError(error_lists)


        #整表是不是只读
        if admin_class.readonly_table:
            self.add_error("__all__","表只读，不能增加和修改")

        self.ValidationError=ValidationError
        #invoke user's customized form validate
        response=admin_class.default_form_validation(self)

        if response:
            error_lists.append(response)

        if error_lists:
            raise ValidationError(error_lists)

    """动态生成modelfrom"""
    class Meta:
        model=admin_class.model
        fields="__all__"
        exclude=admin_class.exclude_field

    attrs={"Meta":Meta}

    _model_form_class=type("DynamicModelForm",(ModelForm,),attrs)#动态创建类
    setattr(_model_form_class,"__new__",__new__) #给类加方法
    setattr(_model_form_class,"clean",default_clean)
    return _model_form_class

