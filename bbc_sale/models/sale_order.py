# -*- coding: utf-8 -*-
from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    remarks = fields.Char()
    missing_stock = fields.Boolean(
        compute='_get_missing_stock')

    @api.multi
    def action_ship_create(self):
        """
        Populate the manual field that registers if the picking's sale order
        has been paid. Additionally, this happens in a custom server action.
        """
        res = super(SaleOrder, self).action_ship_create()
        for sale_order in self:
            if sale_order.invoiced:
                sale_order.picking_ids.write({'x_is_paid': True})
        return res

    @api.multi
    def _get_missing_stock(self):
        print "getting missing_stock for %s orders" % len(self.ids)
        for order in self:
            order.missing_stock = False
            for line in order.order_line:
                if line.product_id.virtual_available < 0:
                    order.missing_stock = True
                    break
