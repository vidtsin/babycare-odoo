# -*- coding: utf-8 -*-
from openerp import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    remarks = fields.Char()
    missing_stock = fields.Boolean(
        compute='_get_missing_stock')

    @api.multi
    def _get_missing_stock(self):
        missing_stock_orders = self.search(
            [('id', 'in', self.ids),
             ('order_line.product_id.virtual_available', '<', 0)])
        for sale in self:
            sale.missing_stock = sale in missing_stock_orders
