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


class Teacher(models.Model):
    _name = "course.teacher"
    className = fields.Char(string=u"你的课程", default=lambda self: self.env['course.session'].search([('name', '=', self.env.user.name)]).course_id)
    name = fields.Char(string=u'姓名', default=lambda self: self.env.user.name)
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    gender = fields.Selection(GENDER, string=u'性别')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')


class Director(models.Model):
    _name = "course.director"
    name = fields.Char(string=u'姓名', default=lambda self: self.env.user.name)
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    gender = fields.Selection(GENDER, string=u'性别')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')


class leave(models.Model):
    _name = 'course.leave'
    subject = fields.Char(string=u'课程', default=lambda self: self.env['course.choice'].search(
        [('name', '=', self.env.user.name)]).className2)
    name = fields.Char(string=u'姓名', default=lambda self: self.env.user.name)
    teacheName = fields.Char(string='任课老师', required=True)
    days = fields.Integer(string=u"请假节数", required=True)
    sumleave = fields.Integer(string=u"请假总节数", default=lambda self: self.env.user.sumdays)
    sumdays = fields.Integer(string=u"课程总节数", default=lambda self: self.env['course.session'].search([('course_id', '=', self.env.user.classname)]).num)
    startdate = fields.Date(string=u"请假日期", required=True)
    reason = fields.Text(string=u"请假事由", required=True)
    request_permit = fields.Boolean(u'申请审核', readonly=True, index=True, track_visibility='onchange')
    get_permit = fields.Boolean(u'审核通过', readonly=True, index=True, track_visibility='onchange')

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
        ('permit', u'审核通过')
    ]
    request_state = fields.Selection(WORKFLOW_STATE_SELECTION2, string='完成情况', default='submit', readonly=True)
    WORKFLOW_STATE_SELECTION3 = [
        ('refuse', '拒绝申请'),
        ('nopermit', '待审批'),
        ('permitted', '审批通过'),
    ]
    permit_state = fields.Selection(WORKFLOW_STATE_SELECTION3, string='审批情况', default='nopermit', readonly=True)

    @api.multi
    def action_permit(self):
        self.write({'request_state': 'permit'})
        self.action_done()
        for record in self:
            record.request_permit = False
            record.get_permit = True

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
        self.write({'permit_state': 'refuse'})

    @api.multi
    def action_nopermit(self):
        self.write({'permit_state': 'nopermit'})

    @api.multi
    def action_permitted(self):
        self.write({'permit_state': 'permitted'})
        self.action_permit()

    @api.multi
    def action_refuse(self):
        self.write({'permit_state': 'refuse'})
        self.action_submit()


class Session(models.Model):
    _name = 'course.session'
    start_date = fields.Date(string="开始时间", default=fields.Date.today)
    seats = fields.Integer(string="容纳人数", default=5)
    color = fields.Integer()  # Kanban视图color字段声明
    course_id = fields.Char(string="课程名", required=True)
    name = fields.Char(string="任课老师", required=True)
    attendee_ids = fields.One2many('course.choice', 'leader_id', string="上课学生")
    num = fields.Integer(string="课程节数", required=True, default=2)
    attendees_count = fields.Integer(string="出席人数", compute='_get_attendees_count', store=True)
    taken_seats = fields.Float(string="选课率", compute='_taken_seats')

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

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
    name = fields.Char(string="课程名", required=True)
    description = fields.Text(u"课程介绍")
    _sql_constraints = [
        ('name_unique',
         'UNIQUE(name)',
         "该课程已经发布"),
    ]


class Choice(models.Model):
    _name = 'course.choice'
    surplus = fields.Char(string=u"剩余数量", default="5")
    className = fields.Many2one('course.zcourse', ondelete='cascade', string=u"选择课程")
    className2 = fields.Char(string=u"确认课程")
    name = fields.Char(string=u'学生姓名', default=lambda self: self.env.user.name)
    info = fields.One2many('course.session', 'name', string=u'相关信息')
    leader_id = fields.Many2one('course.session', string=u'任课老师')
    # test = fields.Float(related="leader_id.taken_seats", store=True, string="选课率")

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

    # 座位约束
    @api.onchange('test')
    def _verify_valid_seats(self):
        if self.test > 100:
            raise exceptions.ValidationError('选课人数超出限制!')
                # self.env['course.session']._verify_valid_seats()
                # if r.leader_id.taken_seats == 100:
                #     raise exceptions.ValidationError('选课人数超出限制!')

class User(models.Model):
    _inherit = "res.users"
    classname = fields.Char(string=u"课程")
    sumdays = fields.Integer(string=u'请假总节数')
