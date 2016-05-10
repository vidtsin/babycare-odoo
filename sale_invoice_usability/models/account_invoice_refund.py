# coding: utf-8
from openerp import api, fields, models


class Refund(models.TransientModel):
    _inherit = 'account.invoice.refund'

    other_invoice_ids = fields.Many2many(
        'account.invoice',
        compute='get_other_invoice_ids',
        string='Related invoices')

    @api.multi
    def get_other_invoice_ids(self):
        self.ensure_one()
        invoice_ids = self.env.context.get('active_ids', [])
        self.other_invoice_ids = self.env['account.invoice'].search([
            ('sale_order_ids.invoice_ids', 'in', invoice_ids),
            ('id', 'not in', invoice_ids)])

    @api.model
    def default_get(self, fields_list):
        res = super(Refund, self).default_get(fields_list)
        if not fields_list or 'other_invoice_ids' in fields_list:
            invoice_ids = self.env.context.get('active_ids', [])
            res['other_invoice_ids'] = self.env['account.invoice'].search([
                ('sale_order_ids.invoice_ids', 'in', invoice_ids),
                ('id', 'not in', invoice_ids)]).ids
        return res
