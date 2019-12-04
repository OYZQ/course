# -*- coding: utf-8 -*-
import base64
import logging

from odoo import api, fields, models
from odoo.modules.module import get_module_resource
from odoo import tools, _

_logger = logging.getLogger(__name__)

GENDER = [
    ('male', u'男'),
    ('female', u'女'),
    ('other', u'其他')
]

MARITAL = [
    ('single', u'单身'),
    ('married', u'已婚'),
    ('cohabitant', u'合法同居'),
    ('widower', u'丧偶'),
    ('divorced', u'离婚')
]

COMPANY = [
    ('normal', u'神动')
]

class Employee(models.Model):
    _name = "ml.employee"
    _description = '''
        员工信息
    '''

    @api.model
    def _default_image(self):
        image_path = get_module_resource('hr', 'static/src/img', 'default_image.png')
        return tools.image_resize_image_big(base64.b64encode(open(image_path, 'rb').read()))

    name = fields.Char(string=u'姓名')

    # image
    image = fields.Binary(string=u"照片", default=_default_image, attachment=True, help=u"上传员工照片，<1024x1024px")
    image_medium = fields.Binary(string=u"中尺寸照片", attachment=True, help="128x128px照片")
    image_small = fields.Binary(string=u"小尺寸照片", attachment=True, help="64x64px照片")

    company_id = fields.Many2one('res.company', string=u'公司')

    gender = fields.Selection(GENDER, string=u'性别')
    country_id = fields.Many2one('res.country', string=u'国籍')
    birthday = fields.Date(string=u'生日')
    marital = fields.Selection(MARITAL, string=u'婚姻状况', default='single')

    # work
    address = fields.Char(string=u'家庭住址')
    mobile_phone = fields.Char(string=u'手机号码')
    work_email = fields.Char(string=u'工作邮箱')
    leader_id = fields.Many2one('ml.employee', string=u'所属上级')
    subordinate_ids = fields.One2many('ml.employee', 'leader_id', string=u'下属')

    note = fields.Text(string=u'备注信息')

    @api.model
    def create(self, values):
        tools.image_resize_images(values)
        return super(Employee, self).create(values)

    @api.multi
    def write(self, values):
        tools.image_resize_images(values)
        return super(Employee, self).write(values)