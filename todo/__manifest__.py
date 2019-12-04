# -*- coding: utf-8 -*-
{
    'name': "todo",

    'summary': """
        Todo, list what you want to do.""",

    'description': """
        Todo App.
    """,

    'author': "Yifchen",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/todo_security.xml',
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/menu.xml',
        'security/ir_rule.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
        'views/menu.xml',
        'views/templates.xml',
    ],
    'application': True,
    # 'sequence': 1
}
