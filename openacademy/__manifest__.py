# -*- coding: utf-8 -*-
{
    'name': "Open Academy",
    'summary': """Manage trainings""",
    'description': """
Open Academy module for managing trainings:
- training courses
- training sessions
- attendees registration
""",
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    # Category 用于在列表中筛选模块
    'category': 'Test',
    'version': '0.1',
    # 填写所有当前模块依赖的其他模块名称
    'depends': ['base', 'board'],
    # 安装模块时必然加载
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/openacademy.xml',
        'views/partner.xml',
        'views/session_board.xml',
        'views/reports.xml',
    ],
    # 只在 demonstration 模式下加载
    'demo': [
        'demo/demo.xml',
    ],
}
