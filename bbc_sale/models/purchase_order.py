# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    remarks = fields.Char()
    missing_stock = fields.Boolean(
        compute='_get_missing_stock')
    free_shipping = fields.Boolean(
        compute='_get_free_shipping',
        search='_search_free_shipping')

    def _search_free_shipping(self, operator, value):
        if operator not in ('=', '==') and not isinstance(value, bool):
            raise UserError(
                'This query on the "free shipping" field is not supported. '
                'You can only search on "= True" or "= False"')
        self.env.cr.execute(
            """
            SELECT id FROM purchase_order po, res_partner rp
                WHERE po.partner_id = rp.id
                    AND amount_total < rp.amount_free_shipping
            """)
        ids = [res_id for res_id, in self.env.cr.fetchall()]
        return [('id', 'in', ids)]

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
