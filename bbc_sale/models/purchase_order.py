# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    remarks = fields.Char()
    missing_stock = fields.Boolean(
        compute='_get_missing_stock',
        search='_search_missing_stock',
        help=('Indicates that virtual stock is below zero, but only for '
              'unconfirmed purchases'))
    free_shipping = fields.Boolean(
        compute='_get_free_shipping',
        search='_search_free_shipping')

    def _get_free_shipping(self):
        for order in self:
            order.free_shipping = (
                order.amount_untaxed >= order.partner_id.commercial_partner_id
                .amount_free_shipping)

    def _search_free_shipping(self, operator, value):
        if operator not in ('=', '==') and not isinstance(value, bool):
            raise UserError(
                'This query on the "free shipping" field is not supported. '
                'You can only search on "= True" or "= False"')
        self.env.cr.execute(
            """
            SELECT po.id FROM purchase_order po, res_partner rp
                WHERE po.partner_id = rp.id
                    AND amount_untaxed >= rp.amount_free_shipping
            """)
        ids = [res_id for res_id, in self.env.cr.fetchall()]
        return [('id', 'in', ids)]

    @api.multi
    def _get_missing_stock(self):
        for order in self:
            order.missing_stock = False
            if order.state not in ('draft', 'sent', 'bid'):
                # Ignored anyway
                continue
            for line in order.order_line:
                if line.product_id.virtual_available < 0:
                    order.missing_stock = True
                    break

    @api.multi
    def _search_missing_stock(self, operator, value):
        if operator not in ('=', '==') and not isinstance(value, bool):
            raise UserError(
                'This query on the "missing stock" field is not supported. '
                'You can only search on "= True" or "= False"')
        self.env.cr.execute(
            """
            SELECT pol.product_id, pol.order_id FROM purchase_order_line pol,
                purchase_order po
            WHERE pol.order_id = po.id
            AND po.state in ('draft', 'sent', 'bid');
            """)
        product_order = self.env.cr.fetchall()
        products = self.env['product.product'].browse(
            [x[0] for x in product_order]).filtered(
            lambda p: p.virtual_available < 0)
        purchase_ids = [x[1] for x in product_order
                        if (x[0] in products.ids) == value]
        return [('id', 'in', purchase_ids)]
