# _*_ coding:utf-8 _*_
__author__ = "shisanjun"

from django import template
from django.core.exceptions import FieldDoesNotExist
from django.utils.safestring import mark_safe
from django.utils.timezone import datetime,timedelta #使用django的时间，settiong中的配置,间隔timedelta默认是天
register=template.Library()

@register.simple_tag
def render_app_name(admin_class):
    """
    返回model名称
    :param admin_class:
    :return:
    """
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_query_sets(admin_class):
    """
    返回所有数据
    """
    # for i in admin_class.model.objects.all():
    #     print(i)
    return admin_class.model.objects.all()

@register.simple_tag
def build_table_row(request,obj,admin_class):
    """
    显示数据列表
    :param obj:
    :param admin_class:
    :return:
    """
    row_ee=""
    for index,column in enumerate(admin_class.list_display):
        try:
            field_obj=obj._meta.get_field(column)#取字段

            if field_obj.choices:  #判断字段是否是choice
                column_data=getattr(obj,"get_%s_display"%column)()
            else:
                column_data=getattr(obj,column)

            if type(column_data).__name__ =="datetime":#判断是不是时间类型,做时候类型转换
                column_data=column_data.strftime("%Y-%m-%d %H%M%S")

            if index==0:#跳转到修改页
               column_data= '<a href="{request_path}/{obj_id}/change/">{data}</a>'.format(
                    request_path=request.path_info,
                    obj_id=obj.id,
                    data=column_data
               )

        except FieldDoesNotExist as e:
            if hasattr(admin_class,column):
                column_func=getattr(admin_class,column)
                #初始化
                admin_class.instance=obj
                admin_class.request=request
                column_data=column_func()

        row_ee+="<td>%s</td>" %column_data

    return mark_safe(row_ee)

@register.simple_tag
def render_page_ele(loop_count,query_set,filter_conditions):
    """
    显示页码
    """
    #上次减缩的过滤条件
    filters=""
    for k,v in filter_conditions.items():
        filters+="&%s=%s" %(k,v)

    #代表这是前两个页或者最后两页
    if loop_count<3 or loop_count>query_set.paginator.num_pages-2:

        ele_class=""
        if query_set.number==loop_count:
            ele_class="active"
        ele='<li class=%s><a  href="?page=%s%s">%s</a><li>'%(ele_class ,loop_count,filters,loop_count)



    if abs(query_set.number-loop_count)<=1:#显示当前页的前后页
        ele_class=""
        if query_set.number==loop_count:
            ele_class="active"
        ele='<li class=%s><a  href="?page=%s%s">%s</a><li>'%(ele_class ,loop_count,filters,loop_count)
        return mark_safe(ele)
    else:
        return ''

@register.simple_tag
def render_filter_ele(condion,admin_class,filter_conditions):
    """
    实现条件过滤及渲染
    :param column:
    :param admin_class:
    :return:
    """
    #select_ele="<select class='form-control' name='%s'><option value=''>-----</option>" %condion #注意value=''
    #注意value
    select_ele='''
    <select class="form-control" name="{filter_field}"><option value="">-----</option>
   '''

    field_obj=admin_class.model._meta.get_field(condion)
    """field_obj.choices
        (1,"转介绍"),
        (2,"QQ群"),
        (3,"官网"),
        (4,"百度推广"),
        (5,"51cto"),
        (6,"知呼"),
        (7,"市场推广"),
    """

    #choice类型数据
    if field_obj.choices:
        selected=""
        for choice_item in field_obj.choices:
            #判断默认值，比如filter_conditions{source=2&consultant=&tag=}；condion是KEY
            if filter_conditions.get(condion)==str(choice_item[0]):
                selected="selected"
            select_ele+="<option value='%s' %s>%s</option>" %(choice_item[0],selected,choice_item[1])
            selected=""

    #外键数据
    if type(field_obj).__name__=="ForeignKey": #显示外键数据
        selected=""
        for index,choice_item in enumerate(field_obj.get_choices()[1:]):#所有外键的数据
            if filter_conditions.get(condion)==str(choice_item[0]): #判断默认值，比如filter_conditions{source=2&consultant=&tag=}；condion是KEY
                selected="selected"
            select_ele+="<option value='%s' %s>%s</option>" %(index+1,selected,choice_item[1]) #index是从0开始
            selected=""
    #日期类型过滤
    if type(field_obj).__name__ in ["DateTimeField","DateField"]:
        date_ele=[]
        today_ele=datetime.now().date()#一天，从0点开始

        date_ele.append(["昨天",datetime.now().date()-timedelta(days=1)])
        date_ele.append(["近7天",datetime.now().date()-timedelta(days=7)])
        date_ele.append(["本月",today_ele.replace(1)])#本月
        date_ele.append(["近30天",datetime.now().date()-timedelta(days=30)])
        date_ele.append(["近90天",datetime.now().date()-timedelta(days=90)])
        date_ele.append(["近365天",datetime.now().date()-timedelta(days=360)])
        date_ele.append(["今年",today_ele.replace(month=1,day=1)])#近一年
        selected=""
        for item in date_ele:
            select_ele+="<option value='%s' %s>%s</option>" %(item[1],selected,item[0])

        filter_field_name="%s__gte"%condion
    else:
        filter_field_name=condion


    select_ele+="</select>"

    select_ele=select_ele.format(filter_field=filter_field_name)
    return mark_safe(select_ele)


@register.simple_tag
def build_paginators(query_set,filter_condions,previous_orderby,serach_text):
    """
    返回整个分页元素
    :param queryset:
    :param filter_condions:
    :return:
    """
    #搜索条件
    filters=""
    for k,v in filter_condions.items():
        filters+="&%s=%s" %(k,v)

    added_dot_ele=False
    page_ele=""
    for page_num in query_set.paginator.page_range:
        #显示最前两个页或者最后两页
        # print(page_num)
        if page_num<3 or page_num>query_set.paginator.num_pages-2:
            ele_class=""
            if query_set.number==page_num:
                ele_class="active"
            #previous_orderby为上一页下一页的时候排序还在传递参数o
            page_ele+='<li class=%s><a href="?page=%s%s&o=%s&_q=%s">%s</a><li>'%(ele_class ,page_num,filters,previous_orderby,serach_text,page_num)

        #显示当前页的前后1页
        elif abs(query_set.number-page_num)<=1:
            ele_class=""
            if query_set.number==page_num:
                #added_dot_ele=False说明当前页的前面有超过2页，现在设置后面False当前页面的后面还需要显示..，所以要设置为False
                added_dot_ele=False
                ele_class="active"

            page_ele+='<li class=%s><a  href="?page=%s%s">%s</a><li>'%(ele_class ,page_num,filters,page_num)
        else:
            #加...
            if not added_dot_ele:
                page_ele+='<li><a>...</a></li>'
                added_dot_ele=True

    return mark_safe(page_ele)

@register.simple_tag
def build_table_header_column(column, order_by_key,filter_conditions,admin_class):

    #上次减缩的过滤条件
    filters=""
    for k,v in filter_conditions.items():
        filters+="&%s=%s" %(k,v)

    sort_icon=""
    #第一次访问没有order_by_key，所以会是空，需要把column返回
    if order_by_key:
        #箭头图标显示
        if order_by_key.startswith("-"):
            sort_icon='<i class="fa fa-angle-down"></i>'
        else:
            sort_icon='<i class="fa fa-angle-up"></i>'
        if order_by_key.strip("-")==column:
            order_by_key=order_by_key

        else:
            order_by_key=column
            #默认是没有图标的
            sort_icon=""
    else:
        order_by_key=column


    #判读为空显示的字段
    try:
        column_verbose_name=admin_class.model._meta.get_field(column).verbose_name

    except FieldDoesNotExist as e:
        column_verbose_name=getattr(admin_class,column).display_name
        #去除空标签标题链接
        ele="<th><a href='javascript:void();'>%s</a></th>"%column_verbose_name

        return mark_safe(ele)

    ele="""<td><a href="?%s&o=%s">%s</a>%s</td>"""%(filter_conditions,
                                                    order_by_key,column_verbose_name,sort_icon)
    # print(ele)
    return mark_safe(ele)

@register.simple_tag
def get_model_name(admin_class):
    """
    返回应用名
    """
    return admin_class.model._meta.verbose_name

@register.simple_tag
def get_m2m_obj_list(admin_class,field,form_obj):
    #返回M2M待选数据
    #表结构对象的某个字段
    field_obj=getattr(admin_class.model,field.name)

    all_obj_list=field_obj.rel.to.objects.all()
    #单条数据的对象中的某个字段
    if form_obj.instance.id:#form_obj.instance.id为空说明说明是新
        obj_instance_field=getattr(form_obj.instance,field.name)
    else:#没有说明是新增（创建新的记录）
        return all_obj_list


    selected_obj_list=obj_instance_field.all()#多对多，取所有数据
    standby_obj_list=[]
    for obj in all_obj_list:
        if obj not in selected_obj_list:
            standby_obj_list.append(obj)

    return standby_obj_list

@register.simple_tag
def print_obj_filed(form_obj):
    pass

@register.simple_tag
def get_m2m_selected_obj_list(form_obj,field):
    #返回已选择的m2m的数据
    if form_obj.instance.id:
        field_obj=getattr(form_obj.instance,field.name)
        return field_obj.all()

def recursive_related_objs_lookup(objs):
    # model_name = objs[0]._meta.model_name
    ul_ele = "<ul>"
    print(type(objs))
    for obj in objs:
        li_ele = '''<li> %s: %s</li>''' % (obj._meta.verbose_name, obj.__str__().strip("<>"))
        ul_ele += li_ele
        #print(li_ele)

        # #for local many to many
        sub_ul_ele = "<ul>"
        for m2m_field in obj._meta.local_many_to_many: #把所有跟这个对象直接关联的m2m字段取出来
            m2m_field_obj = getattr(obj, m2m_field.name) #getattr(customer,'tag')
            for o in m2m_field_obj.select_related(): #cusomter.tags.select_related()
                li_ele = '''<li> %s: %s</li>''' % (m2m_field.verbose_name, o.__str__().strip("<>"))
                sub_ul_ele += li_ele

            sub_ul_ele += "</ul>"
            ul_ele += sub_ul_ele

        for related_obj in obj._meta.related_objects:
            #print("--->")
            # if "ManyToeRel" not in related_obj.__repr__():
            #     continue

            if "ManyToManyRel" in related_obj.__repr__():
                print("ManyManyRel", related_obj.get_accessor_name())
                if hasattr(obj, related_obj.get_accessor_name()):#hasattr(customer)
                    accessor_obj = getattr(obj, related_obj.get_accessor_name())
                    #上面相当于customer.enrollment_set
                    if hasattr(accessor_obj, "select_related"):
                        target_obj = accessor_obj.select_related()

                        sub_ul_ele ="<ul style='color:red'>"
                        for o in target_obj:
                            li_ele = '''<li> %s: %s</li>''' % (o._meta.verbose_name, o.__str__().strip("<>"))
                            sub_ul_ele += li_ele
                    sub_ul_ele += "</ul>"
                    ul_ele += sub_ul_ele


            elif hasattr(obj, related_obj.get_accessor_name()):
                accessor_obj = getattr(obj, related_obj.get_accessor_name())
                #print(accessor_obj)

                if hasattr(accessor_obj, "select_related"):
                    target_obj = accessor_obj.select_related()
                else:
                    target_obj = accessor_obj

                #print(target_obj)
                if len(target_obj) > 0:
                    nodes = recursive_related_objs_lookup(target_obj)
                    ul_ele += nodes

    ul_ele += "</ul>"
    #print(ul_ele)
    return ul_ele


@register.simple_tag
def display_all_related_objs(objs):
    # objs = [objs, ]

    if objs:
        # module_class = objs[0]._meta.model
        # mode_name = objs[0]._meta.model_name
        return mark_safe(recursive_related_objs_lookup(objs))