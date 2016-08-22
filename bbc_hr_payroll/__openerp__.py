# coding: utf-8
# Copyright (C) 2016 Opener B.V. <https://opener.am>
# @author Stefan Rijnhart <stefan@opener.am>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Babycare Payroll customizations',
    'category': 'Human Resources',
    'version': '8.0.1.0',
    'author': 'Opener B.V.',
    'website': 'https://opener.am',
    'depends': [
        'hr_payroll',
    ],
    'data': [
        'views/hr_payslip.xml',
        'views/menu.xml',
        'security/ir_rule.xml',
        'security/ir.model.access.csv',
    ],
}
