# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TodoReport(models.Model):
    _name = 'todo.task.report'
    _inherit = 'todo.task'
    _description = '待办报表'
    _auto = False

    def init(self):
        self.env.cr.execute("""
        CREATE OR REPLACE VIEW todo_task_report AS 
        ( SELECT * FROM todo_task WHERE activate = True)
        """)
