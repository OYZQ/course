# -*- coding: utf-8 -*-

from odoo import models, fields, api

GENDER = [
    ('male', u'男'),
    ('female', u'女'),
    ('other', u'其他')
]

STATUS = [
    ('DIRECTOR', u'教导主任'),
    ('TEACHER', u'老师'),
    ('STUDENT', u'学生')
]

NUM = 5

class Course(models.Model):
    _name = 'course.course'

    name = fields.Char(string=u"课程名", required=True)
    description = fields.Text(u"课程介绍")
    responsible_id = fields.Many2one('res.users', ondelete='set null', string=u"任课老师", index=True)

class Employee(models.Model):
    _name = "course.employee"
    name = fields.Char(string=u'姓名')
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    gender = fields.Selection(GENDER, string=u'性别')
    status = fields.Selection(STATUS, string=u'职位')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')

class Teacher(models.Model):
    _name = "course.teacher"
    name = fields.Char(string=u'姓名')
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    gender = fields.Selection(GENDER, string=u'性别')
    status = fields.Selection(STATUS, string=u'职位')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')

class Director(models.Model):
    _name = "course.director"
    name = fields.Char(string=u'姓名')
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    gender = fields.Selection(GENDER, string=u'性别')
    status = fields.Selection(STATUS, string=u'职位')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')

class leave(models.Model):
    _name = 'course.leave'
    name = fields.Many2one('course.employee', string=u"申请人", required=True)
    subject = fields.Many2one('course.zcourse', string=u"课程", required=True)
    days = fields.Integer(string=u"天数")
    startdate = fields.Date(string=u"开始日期")
    enddate = fields.Date(string=u"截至日期")
    reason = fields.Text(string=u"请假事由")
    tstate = fields.Selection(
                [('O', '通过'),
                ('l', '不通过'),
                ('2', '未审核')],
                u'老师意见', default='2')
    dstate = fields.Selection(
                [('O', '通过'),
                ('l', '不通过'),
                ('2', '未审核')],
                u'主任意见', default='2')

class Session(models.Model):
    _name = 'course.session'
    start_date = fields.Date(string="开始时间", default=fields.Date.today)
    seats = fields.Integer(string="容纳人数", default=10)
    active = fields.Boolean(default=True)
    color = fields.Integer()  # Kanban视图color字段声明
    instructor_id = fields.Many2one('course.director', string="教导主任", required=True)
    course_id = fields.Many2one('course.zcourse', ondelete='cascade', string="课程名", required=True)
    name = fields.Many2one('course.teacher', string="任课老师", required=True)
    attendee_ids = fields.Many2many('course.employee', string="上课学生")
    num = fields.Integer(string="课程节数", required=True, default=2)
    # Graph视图字段声明
    attendees_count = fields.Integer(string="出席人数", compute='_get_attendees_count', store=True)

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)

    # 座位比例计算
    taken_seats = fields.Float(string="到课率", compute='_taken_seats')

    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    # 日历
    end_date = fields.Date(string="截至时间", store=True, compute='_get_end_date', inverse='_set_end_date')

    # 课程节数约束
    @api.onchange('num')
    def _taken_num(self):
        if self.num < 1:
            return {
                'warning': {
                    'title': "课程节数太少",
                    'message': "课程节数必须大于0",
                },
            }

    # 座位约束
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': "座位数字不对",
                    'message': "可用座位数必须大于人",
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': "参加学生太多太多",
                    'message': "建议你增加座位或取消多余的与会者",
                },
            }

class Zcourse(models.Model):
    _name = 'course.zcourse'
    name = fields.Char(string="课程名", required=True)
    description = fields.Text(u"课程介绍")

class Choice(models.Model):
    _name = 'course.choice'
    surplus = fields.Integer(string=u"剩余数量")
    className = fields.Many2one('course.zcourse', ondelete='cascade', string=u"已选课程", required=True)
    # studentName = fields.Many2one('course.employee', ondelete='cascade', string=u"学生姓名", required=True)
    name = fields.Many2one('course.employee', string=u"学生姓名", required=True)
    info = fields.One2many('course.session', 'name', string=u'相关信息')