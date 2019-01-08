# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.tools import float_compare


class Task(models.Model):
    _name = 'task'
    _order = 'id desc'
    _description = 'Task'

    name = fields.Char('任务名称', copy=False, required=True)
    code = fields.Char('任务编号', copy=False)
    description = fields.Html('问题描述')
    solution = fields.Html('解决思路')
    type = fields.Char('任务类型', default="开发")
    state = fields.Selection([('0', '未开始'), ('1', '进行中'), ('2', '已完成'), ('3', '补充修改'), ('4', '已关闭')],
                             string='状态', siHtmlze=1, help='Priority', default='0', required=True,)
    priority = fields.Selection([('0', '非常紧急'), ('1', '紧急'), ('2', '一般'), ('3', '正常'), ('4', '不太着急')],
                                string='优先级', size=1, help='Priority', default='3', required=True)
    module = fields.Char('模块', required=True, default="/")
    project = fields.Char('项目', required=True, default="/")
    propose_people = fields.Char('由谁创建', default="/")
    business_person = fields.Char('由谁负责', default="/")
    working_hours = fields.Float('预估工时', required=True, default=0)
    actual_hours = fields.Float('实际工时', default=0)
    start_time = fields.Date('预计开始时间', required=True, default=fields.Date.today())
    end_time = fields.Date('预计结束时间')
    actual_start_time = fields.Date('实际开始时间', required=True, default=fields.Date.today())
    actual_end_time = fields.Date('实际结束时间')
