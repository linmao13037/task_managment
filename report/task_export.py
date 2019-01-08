# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import base64
import xlwt
from io import BytesIO


class TaskExport(models.TransientModel):
    _name = "task.export"
    _description = "Task Export"

    file = fields.Binary('文件')

    def generate_excel(self, task_ids):
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('任务清单')
        worksheet.col(0).width = (10 * 367)  # 设置表格的宽度
        worksheet.col(1).width = (30 * 367)
        worksheet.col(2).width = (15 * 367)
        worksheet.col(3).width = (15 * 367)

        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = '微软雅黑'  # 字体
        font.bold = True   # 加粗
        font.height = 20 * 10  # 字体大小
        style.font = font  # 为样式设置字体

        # add header
        header = ['任务号', '任务名称', '开始时间', '结束时间']
        for col in range(len(header)):
            worksheet.write(0, col, header[col], style)

        # add data
        for row in range(1, len(task_ids) + 1):
            task_id = task_ids[row - 1]
            worksheet.write(row, 0, task_id.code if task_id else '')
            worksheet.write(row, 1, task_id.name if task_id else '')
            worksheet.write(row, 2, str(task_id.start_time).replace('-', '/') if task_id.start_time else '')
            worksheet.write(row, 3, str(task_id.end_time).replace('-', '/') if task_id.end_time else '')

        # save
        buffer = BytesIO()
        workbook.save(buffer)
        return base64.encodebytes(buffer.getvalue())

    @api.multi
    def action_export_data(self):
        context = dict(self._context or {})
        task_ids = context.get('active_ids')
        task_ids = self.env['task'].browse(task_ids)

        res = self.create({'file': self.generate_excel(task_ids)})

        value = dict(
            type='ir.actions.act_url',
            target='self',
            url='/web/content?model=%s&id=%s&field=file&download=true&filename=task.xls' % (self._name, res.id),
        )
        return value
