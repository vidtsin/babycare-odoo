# -*- coding: utf-8 -*-
from openerp import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_state = fields.Selection(
        related='product_id.state')
    virtual_available = fields.Float(
        related='product_id.virtual_available')

    @api.multi
    def onchange_product_id(
            self, pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=False, fiscal_position_id=False,
            date_planned=False, name=False, price_unit=False,
            state='draft'):
        res = super(PurchaseOrderLine, self).onchange_product_id(
            pricelist_id, product_id, qty, uom_id, partner_id,
            date_order=date_order, fiscal_position_id=fiscal_position_id,
            date_planned=date_planned, name=name, price_unit=price_unit,
            state=state)
        if product_id and res.get('value'):
            product = self.env['product.product'].browse(product_id)
            res['value'].update(
                virtual_available=product.virtual_available,
                product_state=product.state)
        return res
