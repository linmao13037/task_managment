# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo.tools import float_is_zero, float_compare, pycompat
from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.exceptions import UserError, ValidationError
import base64
import xlrd
from io import BytesIO


class TaskImport(models.TransientModel):
    _name = "task.import"
    _description = "Task Import"

    file = fields.Binary('文件')


    @api.multi
    def action_import(self):
        """
        导入excel文件,按行读取数据并处理
        :return: 导入结果视图
        """
        if not self.file:
            return
        book = xlrd.open_workbook(file_contents=base64.decodebytes(self.file))
        sh = book.sheet_by_index(0)
        res_id = []
        for rx in range(1, sh.nrows):
            row = sh.row(rx)
            try:
                res = self.check_and_save(row)
            except:
                raise ValidationError(_('Excel文件错误，请检查excel文件是否符合导入模板格式!'))

            res_id.append(res)

        # 跳转到导入结果视图
        tree_view_id = self.env.ref('task_management.task_tree_view')
        form_view_id = self.env.ref('task_management.task_form_view')
        return {
            'name': _('任务管理'),
            'view_type': 'form',
            'view_mode': 'tree, form',
            'res_model': 'task',
            'views':  [[tree_view_id.id, 'list'], [form_view_id.id, 'form']],
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', res_id)],
            'context': {'clear_breadcrumbs': True}
        }

    def check_and_save(self, row):
        """
        校验并保存
        :param row: excel行
        :return: 任务对象id
        """
        develop_person = row[1].value if row[1].value else False
        code = row[2].value if row[2].value else False
        name = row[3].value if row[3].value else False
        start_time = datetime.strptime(str(row[4].value).strip(), '%Y/%m/%d') if row[4].value else False
        end_time = datetime.strptime(str(row[5].value).strip(), '%Y/%m/%d') if row[5].value else False
        working_hours = row[6].value if row[6].value else False
        actual_hours = row[7].value if row[7].value else False

        if develop_person and name:
            pass
        else:
            raise ValidationError("姓名和任务标题不能为空！")

        vals = {
                'develop_person': develop_person,
                'code': code,
                'name': name,
                'start_time': start_time,
                'end_time': end_time,
                'working_hours': working_hours,
                'actual_hours': actual_hours,
            }

        return self.env['task'].create(vals).id
