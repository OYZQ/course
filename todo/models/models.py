# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class TodoTask(models.Model):
    _name = 'todo.task'
    _inherit = 'mail.thread'
    _description = '我的待办'

    name = fields.Char(u'标题')
    category_id = fields.Many2one('todo.category', string=u'分类')
    is_done = fields.Boolean(u'已完成', default=False, track_visibility='onchange')
    content = fields.Html(u'详细内容', strip_style=True)
    progress_report = fields.Html(u'进度汇报', strip_style=True)
    priority = fields.Selection([
        ('normal', '普通'),
        ('urgency', '紧急')
    ], default='normal', required=True, string='紧急程度')
    is_expired = fields.Boolean(u'已过期', default=False, compute='_compute_is_expired', readonly=True)
    count_expired = fields.Integer(u'超期数量', compute='_compute_count_expired', readonly=True)
    deadline = fields.Datetime(u'截止时间')
    create_date = fields.Date(u'创建日期', required=True, readonly=True, index=True, default=fields.Date.today)
    creator_id = fields.Many2one('res.users', string='安排人', default=lambda s: s.env.uid, required=True, readonly=True)
    coordinator_id = fields.Many2one('res.users', string='协调人', default=lambda s: s.env.uid)
    executor_id = fields.Many2one('res.users', string='执行人')
    activate = fields.Boolean(u'已激活', required=True, readonly=True, index=True)
    request_permit = fields.Boolean(u'申请审核', readonly=True, index=True,
                                    track_visibility='onchange')
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
        self.write({'request_state': 'review'})
        self.action_nopermit()
        for record in self:
            record.request_permit = True

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
        users_group = self.env['res.groups'].search([('name', '=', '管理员')]).users
        for ids in users_group:
            if self._uid == ids.id:
                self.write({'task_state': 'cancel'})

    @api.multi
    def action_nopermit(self):
        self.write({'permit_state': 'nopermit'})

    @api.multi
    def action_permitted(self):
        users_group = self.env['res.groups'].search([('full_name', 'ilike', '待办事项 / 管理员')]).users
        ids = []
        for user in users_group:
            ids.append(user.id)
        if self._uid in ids:
            for record in self:
                if record.request_permit:
                    self.write({'permit_state': 'permitted'})
                    self.action_permit()
        else:
            raise UserError('你没有权限')

    @api.multi
    def action_refuse(self):
        self.write({'permit_state': 'refuse'})
        self.action_submit()

    @api.depends('deadline')
    @api.multi
    def _compute_is_expired(self):
        for record in self:
            if record.deadline:
                record.is_expired = record.deadline < fields.Datetime.now()
            else:
                record.is_expired = False

    @api.depends('deadline')
    @api.multi
    def _compute_count_expired(self):
        for record in self:
            if record.deadline:
                if record.deadline < fields.Datetime.now():
                    record.count_expired += 1


class TodoCategory(models.Model):
    _name = 'todo.category'
    _description = '分类列表'

    name = fields.Char(u'分类名')
    task_ids = fields.One2many('todo.task', 'category_id', string='待办事项')
    parent_id = fields.Many2one('todo.category', string='上级', index=True)
    count = fields.Integer(u'任务数量', compute='_compute_task_count')

    @api.depends('task_ids')
    @api.multi
    def _compute_task_count(self):
        for record in self:
            record.count = len(record.task_ids)


class TodoSecurity(models.Model):
    _inherit = 'ir.actions.server'

    groups_id = fields.Many2many('res.groups', 'ir_act_server_group_rel', 'act_id', 'gid', string='权限群组')


class TodoUserGroups(models.Model):
    _inherit = 'res.groups'
