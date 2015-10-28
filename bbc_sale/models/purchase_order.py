# -*- coding: utf-8 -*-
from openerp import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    remarks = fields.Char()
    missing_stock = fields.Boolean(
        compute='_get_missing_stock')

    @api.multi
    def _get_missing_stock(self):
        for order in self:
            if order.state not in ('draft', 'sent', 'bid'):
                # Ignored anyway
                continue
            order.missing_stock = False
            for line in order.order_line:
                if line.product_id.virtual_available < 0:
                    order.missing_stock = True
                    break
