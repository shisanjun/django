# _*_ coding:utf-8 _*_
__author__ = "shisanjun"

# 0:absolute url,1:relate url

perm_dict = {
    'can_access_my_course': {
        'url_type': 0,
        'url': 'student_index',  # url name
        'method': "GET",
        'args': [],
    },
    'can_access_customer': {
        'url_type': 1,
        'url': 'kindadmin/crm/customer',
        'method': "GET",
        'args': [],
    },
    'can_access_customer_detail': {
        'url_type': 0,
        'url': 'table_change',
        'method': "GET",
        'args': [],
    },
    'can_access_homework': {
        'url_type': 0,
        'url': 'homework',
        'method': "GET",
        'args': [],
    },
    'can_access_homework_detail': {
        'url_type': 0,
        'url': 'homework_detail',
        'method': "GET",
        'args': ["courserecord_id", ],
    },
    'can_port_homework_detail': {
        'url_type': 0,
        'url': 'homework_detail',
        'method': "POST",
        'args': ["courserecord_id", ],
    },
}
