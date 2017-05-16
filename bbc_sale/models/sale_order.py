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
        for order in self:
            order.missing_stock = False
            for line in order.order_line:
                if line.product_id.virtual_available < 0:
                    order.missing_stock = True
                    break

    @api.multi
    def _get_fiscal_position(self, partner):
        country = partner.country_id
        if not country:
            return False
        ref = 'bbc_sale.fispos_world'
        if country == self.env.ref('base.nl'):
            ref = 'bbc_sale.fispos_nl'
        elif country in self.env.ref('base.europe').country_ids:
            # Explicitely no intracom in any case. Handled manually.
            ref = 'bbc_sale.fispos_eu'
        return self.env.ref(ref)

    @api.model
    def create(self, vals):
        res = super(SaleOrder, self).create(vals)
        if not vals.get('fiscal_position'):
            fiscal_position = self._get_fiscal_position(
                res.partner_shipping_id)
            if fiscal_position:
                res.fiscal_position = fiscal_position
        return res

    @api.multi
    def onchange_delivery_id(
            self, company_id, partner_id, delivery_id, fiscal_position):
        res = super(SaleOrder, self).onchange_delivery_id(
            company_id, partner_id, delivery_id, fiscal_position)
        fiscal_position = self._get_fiscal_position(
            self.env['res.partner'].browse(delivery_id))
        if fiscal_position:
            res.setdefault('value', {})['fiscal_position'] = fiscal_position.id
        return res
