from odoo import api, fields, models


# 引入odoo内置的板块

class Person(models.Model):
    _name = 'person.mes'
    # 相当于给了此模型一个唯一id，之后很多地方需要用到
    _description = 'persons information'
    # 仅作为描述
    _inherit = ['mail.thread']
    # 引入mail
    person_id = fields.Char(
        string='人员编号',
        index=True,
        readonly=True,
        default='自动生成'
    )

    # 定义字段person_id，类型为Char，标题显示string，标记索引index，只读readonly，默认值default
    @api.model
    def create(self, vals):
        vals['person_id'] = self.env['ir.sequence'].next_by_code('person.mes') or ''
        return super(Person, self).create(vals)

    # 调用内置api重写create方法

    image = fields.Binary(
        '头像'
    )
    # name = fields.Char(
    #     '姓名',
    #     required=True,
    #     help='您的姓名'
    # )
    description = fields.Text(
        '备注'
    )
    register_date = fields.Date(
        '入职日期',
        default=lambda self: fields.Date.today(),
        required=True
    )
    Iscollege = fields.Boolean(
        '是否为大学生',
        default=True,
        required=True
    )
    earn_money = fields.Float(
        '营业额',
        required=True,
        digits=(12, 3),

    )
    # digits定义数字总长和小数部分的位数
    self_intro = fields.Html(
        '自我简介'
    )
    department = fields.Selection(
        [
            ('1', '财务部'),
            ('2', '人力资源部'),
            ('3', '技术部')
        ],
        string='所属部门',
        required=True,
        default='1'
    )
    name = fields.Many2one(
        'res.partner',
        string='人员',
        required=True,
    )

    person_recommend = fields.Many2many(
        'res.partner',
        string='推荐人员',
        required=True,

    )
    state = fields.Selection(
        [
            ('edit', '编辑'),
            ('check', '审批中'),
            ('pass', '通过'),
            ('fail', '失败'),
        ],
        string='状态', default='edit', readonly=True, copy=False, track_visibility='onchange'
    )

    def button_submit(self):
        return self.write({"state": "check"})

    def button_pass(self):
        return self.write({"state": "pass"})

    def button_fail(self):
        return self.write({"state": "fail"})

    salary_month = fields.Float(
        '月薪',
        required=True,
    )
    work_month = fields.Integer(
        '工作时长(月)',
        default=0
    )
    salary_total = fields.Float(
        '总薪水',
        compute="count_total",
        store=True,
        readonly=True
    )

    @api.one
    @api.depends('salary_month', 'work_month')  # depend的字段值一旦发生变化，就会触发该函数，从而更新compute字段值。
    def count_total(self):
        self.salary_total = self.salary_month * self.work_month
