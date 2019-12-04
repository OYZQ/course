# -*- coding: utf-8 -*-
{
    'name': 'Employee',
    'version': '12.0.1.0',
    'summary': '对员工的基本信息，部门和职位进行管理',
    'description': '''
        员工管理模块
    ''',
    'author': 'ouyang',
    'sequence': 15,
    'category': 'Uncategorized',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee.xml',
        'views/menu.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'pre_init_hook': '',
    # 'post_init_hook': '',
    # 'uninstall_hook': '',
}