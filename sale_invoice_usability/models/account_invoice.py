# coding: utf-8
from openerp import api, fields, models


class Invoice(models.Model):
    _inherit = 'account.invoice'
    sale_order_ids = fields.Many2many(
        'sale.order',
        'sale_order_invoice_rel',
        'invoice_id',
        'order_id',
        'Sale orders',
        readonly=True)

    @api.model
    def _prepare_refund(
            self, invoice, date=None, period_id=None,
            description=None, journal_id=None):
        """ Associate sale orders of the origin with the refund """
        res = super(Invoice, self)._prepare_refund(
            invoice, date=date, period_id=period_id,
            description=description, journal_id=journal_id)
        res['sale_order_ids'] = [(6, 0, invoice.sale_order_ids.ids)]
        return res
