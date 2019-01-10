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
        worksheet = workbook.add_sheet(str(fields.Date.today()).replace('-', ''), cell_overwrite_ok=True)
        worksheet.col(0).width = (1 * 367)  # 设置表格的宽度
        worksheet.col(1).width = (10 * 367)
        worksheet.col(2).width = (10 * 367)
        worksheet.col(3).width = (40 * 367)
        worksheet.col(4).width = (10 * 367)
        worksheet.col(5).width = (10 * 367)
        worksheet.col(6).width = (10 * 367)
        worksheet.col(7).width = (10 * 367)
        worksheet.col(8).width = (30 * 367)
        # worksheet.col(0).height  = 1  # 设置表格的高度


        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = '等线'  # 字体
        # font.bold = True   # 加粗
        font.height = 20 * 12  # 字体大小
        style.font = font  # 为样式设置字体

        # add header
        header = ['', '姓名','任务号', '任务标题', '开始时间', '结束时间', '评估人天', '实际消耗人天', '备注']
        for col in range(len(header)):
            worksheet.write(0, col, header[col], style)

        # add data
        for row in range(1, len(task_ids) + 1):
            task_id = task_ids[row - 1]
            worksheet.write(row, 0, '', style)
            worksheet.write(row, 1, task_id.develop_person or '', style)
            worksheet.write(row, 2, task_id.code or '', style)
            worksheet.write(row, 3, task_id.name or '', style)
            worksheet.write(row, 4, str(task_id.start_time).replace('-', '/') or '', style)
            worksheet.write(row, 5, str(task_id.end_time).replace('-', '/') or '', style)
            worksheet.write(row, 6, task_id.working_hours or '', style)
            worksheet.write(row, 7, task_id.actual_hours or '', style)
            worksheet.write(row, 8, task_id.remark or '', style)

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
