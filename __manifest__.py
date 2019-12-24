# -*- coding: utf-8 -*-
# This module is used to manage tasks.

{
    'name': 'Task Management',
    'version': '1.0',
    'summary': 'Collect task and manage them',
    'description': "",
    'website': 'https://blog.csdn.net/sinat_23931991',
    'depends': [],
    'category': 'Task Manage',
    'sequence': 13,
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/task.xml',
        'report/task_export.xml',
        'report/task_import.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
