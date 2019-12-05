{
    'name': '培训',
    'description': 'odoo培训',
    'author': 'zhuhua',
    'depends': ['base', 'mail'],
    'application': True,
    'data': [
        # 'security/train_security.xml',
        # 'security/ir.model.access.csv',
        'views/menu.xml',
        'views/person_mes.xml',
        'views/company_mes.xml'
    ],
}