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
    def _get_fiscal_position(self, partner, intra_partner=False):
        country = partner.country_id
        if not country:
            return False
        ref = 'bbc_sale.fispos_world'
        nl = self.env.ref('base.nl')
        if country == nl:
            ref = 'bbc_sale.fispos_nl'
        else:
            europe = self.env.ref('base.europe').country_ids
            if country in europe:
                if (intra_partner and intra_partner.vat and
                        intra_partner.country_id != nl and
                        intra_partner.country_id in europe):
                    ref = 'bbc_sale.fispos_intra'
                else:
                    ref = 'bbc_sale.fispos_eu'
        return self.env.ref(ref)

    @api.model
    def create(self, vals):
        """ Look up fiscal position by shipping address country but don't
        apply intra as these orders typically originate from Magento """
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
        if partner_id and delivery_id:
            fiscal_position = self._get_fiscal_position(
                self.env['res.partner'].browse(delivery_id),
                intra_partner=self.env['res.partner'].browse(partner_id))
            if fiscal_position:
                res.setdefault(
                    'value', {})['fiscal_position'] = fiscal_position.id
        return res
