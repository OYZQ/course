from odoo import models, fields, api


class TodoCategory(models.Model):
    _name = 'todo.category'

    name = fields.Char('name')
    task_ids = fields.One2many('todo.task', 'category_id', string='todo task')
    count = fields.Integer('task number', compute='_compute_task_count')

    @api.depends('task_ids')
    @api.multi
    def _compute_task_count(self):
        for record in self:
            record.count = len(record.task_ids)


class TodoTask(models.Model):
    _name = "todo.task"
    _description = "do task"

    name = fields.Char(string="description", required=True)
    is_done = fields.Boolean(string="todo")
    priority = fields.Selection([
        ('todo', 'todo'),
        ('normal', 'normal'),
        ('urgency', 'urgency')
    ], default='todo', string='jinjicd')
    deadline = fields.Datetime(string="data die")
    is_expired = fields.Boolean(string="guoqi", compute="_compute_is_expired")
    category_id = fields.Many2one('todo.category', string='category')

    @api.depends("deadline")
    @api.multi
    def _compute_is_expired(self):
        for recored in self:
            if recored.deadline:
                recored.is_expired = (recored.deadline < fields.Datetime.now())
            else:
                recored.is_expired = False



