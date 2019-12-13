# -*- coding: utf-8 -*-

from odoo import models, fields, api

class TodoReport(models.Model):
    _name = 'course.leave.report'
    _inherit = 'course.leave'
    _auto = False

    def init(self):
        self.env.cr.execute("""
        CREATE OR REPLACE VIEW todo_task_report AS 
        ( SELECT * FROM todo_task WHERE activate = True)
        """)
