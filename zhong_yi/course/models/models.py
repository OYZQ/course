# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import exceptions

GENDER = [
    ('male', u'男'),
    ('female', u'女'),
    ('other', u'其他')
]
NUM = 5

class Course(models.Model):
    _name = 'course.course'
    name = fields.Char(string=u"课程名", required=True)
    description = fields.Text(u"课程介绍")
    responsible_id = fields.Many2one('res.users', ondelete='set null', string=u"任课老师", index=True)

class Employee(models.Model):
    _name = "course.employee"
    name = fields.Char(string=u'姓名', default=lambda self: self.env.user.name)
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    gender = fields.Selection(GENDER, string=u'性别')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "一个人只能创建一个个人信息")
    ]

class Teacher(models.Model):
    _name = "course.teacher"
    className = fields.Char(string=u"你的课程", default=lambda self: self.env['course.session'].search([('course_id', '=', self.env.user.name)]).name)
    name = fields.Char(string=u'姓名', default=lambda self: self.env.user.name)
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    gender = fields.Selection(GENDER, string=u'性别')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "一个人只能创建一个个人信息")
    ]

class Director(models.Model):
    _name = "course.director"
    name = fields.Char(string=u'姓名', default=lambda self: self.env.user.name)
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    gender = fields.Selection(GENDER, string=u'性别')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "一个人只能创建一个个人信息")
    ]

class leave(models.Model):
    _name = 'course.leave'
    subject = fields.Char(string=u'课程', default=lambda self: self.env['course.choice'].search(
        [('name', '=', self.env.user.name)]).classname)
    name = fields.Char(string=u'姓名', default=lambda self: self.env.user.name)
    teacheName = fields.Char(string='任课老师', required=True)
    days = fields.Integer(string=u"请假节数", required=True)
    sumleave = fields.Integer(string=u"请假总节数", default=lambda self: self.env.user.sumdays)
    sumdays = fields.Integer(string=u"课程总节数", default=lambda self: self.env['course.session'].search([('course_id', '=', self.env.user.classname)]).num)
    startdate = fields.Date(string=u"请假日期", required=True)
    reason = fields.Text(string=u"请假事由", required=True)
    request_permit = fields.Boolean(u'申请审核', readonly=True, index=True, track_visibility='onchange')
    get_permit = fields.Boolean(u'审核通过', readonly=True, index=True, track_visibility='onchange')
    confirm = fields.Boolean(u'是否提交', readonly=True, index=True, track_visibility='onchange')

    # python约束
    @api.constrains('days')
    def _check_days(self):
        for r in self:
            if r.days == 0:
                raise exceptions.ValidationError('请假节数不可以为0!')

    WORKFLOW_STATE_SELECTION = [
        ('draft', u'草稿'),
        ('arrange', u'安排'),
        ('done', u'完成'),
        ('cancel', u'关闭')
    ]
    task_state = fields.Selection(WORKFLOW_STATE_SELECTION, string='状态', default='draft', readonly=True)
    WORKFLOW_STATE_SELECTION2 = [
        ('submit', u'执行中'),
        ('review', u'审核中'),
        ('permit', u'审核结束')
    ]
    request_state = fields.Selection(WORKFLOW_STATE_SELECTION2, string='完成情况', default='submit', readonly=True)
    WORKFLOW_STATE_SELECTION3 = [
        ('refuse', '拒绝申请'),
        ('nopermit', '待审批'),
        ('permitted', '审批通过'),
        ('draft', '草稿'),
    ]
    permit_state = fields.Selection(WORKFLOW_STATE_SELECTION3, string='假条状态', default='draft', readonly=True)

    @api.multi
    def action_permit(self):
        self.write({'request_state': 'permit'})
        self.action_done()
        for record in self:
            record.request_permit = True
            record.get_permit = True
            record.confirm = False

    @api.multi
    def action_review(self):
        for r in self:
            if r.days:
                if (r.sumleave+r.days)/r.sumdays > 0.2:
                    raise exceptions.ValidationError('请假节数超标了!')
                else:
                    self.env.user.sumdays += r.days
        self.action_nopermit()
        for record in self:
            record.request_permit = True
        self.write({'request_state': 'review'})

    @api.multi
    def action_submit(self):
        self.write({'request_state': 'submit'})
        self.action_arrange()
        for record in self:
            record.request_permit = False

    @api.multi
    def action_draft(self):
        self.write({'task_state': 'draft'})
        for record in self:
            record.activate = False

    @api.multi
    def action_arrange(self):
        self.write({'task_state': 'arrange'})
        for record in self:
            record.activate = True

    @api.multi
    def action_done(self):
        self.write({'task_state': 'done'})

    @api.multi
    def action_cancel(self):
        for r in self:
            if r.permit_state == 'permitted' or r.permit_state == 'refuse' or r.permit_state == 'draft':
                print('已经审批或者草稿不可以审批')
                # raise exceptions.ValidationError('已经审批或者草稿不可以审批!')
            else:
                users_group = r.env['res.groups'].search([('full_name', 'ilike', '课程系统 / 学生吖')]).users
                ids = []
                for user in users_group:
                    ids.append(user.id)
                if r._uid in ids:
                    raise exceptions.ValidationError('你没有权限!')
                else:
                    r.write({'permit_state': 'refuse'})

    @api.multi
    def action_nopermit(self):
        self.write({'permit_state': 'nopermit'})

    @api.multi
    def action_permitted(self):
        for r in self:
            if r.permit_state == 'permitted' or r.permit_state == 'refuse' or r.permit_state == 'draft':
                print('已经审批或者草稿不可以审批')
            else:
                users_group = r.env['res.groups'].search([('full_name', 'ilike', '课程系统 / 学生吖')]).users
                ids = []
                for user in users_group:
                    ids.append(user.id)
                if r._uid in ids:
                    raise exceptions.ValidationError('你没有权限!')
                else:
                    r.write({'permit_state': 'permitted'})
                    r.action_permit()

    @api.multi
    def action_refuse(self):
        self.write({'permit_state': 'refuse'})
        self.action_submit()

class Session(models.Model):
    _name = 'course.session'
    start_date = fields.Date(string="开始时间", default=fields.Date.today)
    seats = fields.Integer(string="容纳人数", default=5)
    color = fields.Integer()  # Kanban视图color字段声明
    name = fields.Char(string="课程名", required=True)
    course_id = fields.Char(string="任课老师", required=True)
    attendee_ids = fields.One2many('course.choice', 'leader_id', string="上课学生")
    num = fields.Integer(string="课程节数", required=True, default=2)
    attendees_count = fields.Integer(string="出席人数", compute='_get_attendees_count', store=True)
    taken_seats = fields.Float(string="选课率", compute='_taken_seats')


    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        if self.attendee_ids:
            self.attendees_count = len(self.attendee_ids)

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    # 日历
    end_date = fields.Date(string="截至时间", store=True, compute='_get_end_date', inverse='_set_end_date')

    # 座位约束
    @api.onchange('taken_seats')
    def _verify_valid_seats(self):
        if self.taken_seats > 100:
            raise exceptions.ValidationError('选课人数超出限制!')

class Zcourse(models.Model):
    _name = 'course.zcourse'
    name = fields.Char(string="课程名", related="test.name")
    test = fields.Many2one('course.session', string="课程名", required=True)
    description = fields.Text(u"课程介绍")

    @api.constrains('description')
    def _check_instructor_not_in_attendees(self):
        users = self.env['course.zcourse'].search([])
        ids = []
        for user in users:
            ids.append(user.name)
        print(ids)
        i = 0
        for r in self:
            for id in ids:
                if r.name == id:
                    i += 1
                    print(i)
                    if i >= 2:
                        raise exceptions.ValidationError('不可以重复发布!')

class Choice(models.Model):
    _name = 'course.choice'
    className2 = fields.Char(related="leader_id.course_id", string=u"任课老师")
    name = fields.Char(string=u'学生姓名', default=lambda self: self.env.user.name)
    info = fields.One2many('course.session', 'course_id', string=u'相关信息')
    leader_id = fields.Many2one('course.session', string=u'选择课程', readonly=False)
    classname = fields.Char(related="leader_id.name", string=u"课程名")
    test = fields.Float(related="leader_id.taken_seats", string="选课率", readonly=False)

    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "一个人只能选择一门课程")
    ]
    @api.multi
    def action_classname(self):
        for r in self:
            if r.className2:
                self.env.user.classname = r.className2
        if self.test > 100:
            raise exceptions.ValidationError('选课人数超出限制!')

    # 座位约束
    @api.onchange('test')
    def _verify_valid_seats(self):
        if self.test >= 100:
            raise exceptions.ValidationError('选课人数超出限制!')

class User(models.Model):
    _inherit = "res.users"
    classname = fields.Char(string=u"课程")
    sumdays = fields.Integer(string=u'请假总节数')
