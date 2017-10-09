# -*- coding: utf-8 -*-
from openerp import models, fields


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    product_id = fields.Many2one(
        domain=[('sale_ok', '=', True), ('consu_single_attr', '=', False)])
