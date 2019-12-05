# -*- coding: utf-8 -*-
{
    'name': "course",

    'summary': "课程系统",

    'description': "课程系统：用户分为三个角色：教导主任老师，学生。。。",

    'author': "ouyang",
    'website': "http://www.oyzq.club",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/course_security.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}