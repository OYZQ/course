from odoo import fields, models

class Company(models.Model):
    _name = 'company.mes'
    _description = '合作公司看板'

    name = fields.Char(
        '公司名称'
    )

    logo = fields.Binary(
        '公司商标'
    )

    phone_number = fields.Char(
        '联系电话'
    )

    website = fields.Char(
        '公司网站'
    )

    intro = fields.Html(
        '公司简介'
    )

    person_in_charge = fields.Many2one(
        'person.mes',
        string="负责人"
    )

    # 使用看板视图之前,需要添加几个字段
    # 用于标记 优先级
    priority = fields.Selection(
        [('0','低级'),
         ('1','中级'),
         ('2','高级')
        ],
        '合作等级',
        default='1'
    )
    color = fields.Integer()

