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

class test(models.Model):
    _name = 'test.test'
    name = fields.Char(string="申请人")
    days = fields.Integer(string="天数")
    startdate = fields.Date(string="开始日期")
    enddate = fields.Date(string="截至日期")
    reason = fields.Text(string="请假事由")

class Session(models.Model):
    _name = 'course.session'

    start_date = fields.Date(string="开始时间", default=fields.Date.today)
    # duration = fields.Float(string="持续时间", digits=(6, 2), help="Duration in days")
    seats = fields.Integer(string="座位数量")
    active = fields.Boolean(default=True)
    color = fields.Integer()  # Kanban视图color字段声明
    instructor_id = fields.Many2one('course.director', string="教导主任", required=True)
    course_id = fields.Many2one('course.zcourse', ondelete='cascade', string="课程名", required=True)
    name = fields.Many2one('course.teacher', string="任课老师", required=True)
    attendee_ids = fields.Many2many('res.partner', string="上课学生")
    num = fields.Integer(string="课程节数", required=True)
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

    # 座位约束
    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        if self.seats < 0:
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of available seats may not be negative"),
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }

class Zcourse(models.Model):
    _name = 'course.zcourse'

    name = fields.Char(string="课程名", required=True)
    description = fields.Text(u"课程介绍")
    responsible_id = fields.Many2one('res.users', ondelete='set null', string=u"任课老师", index=True)
