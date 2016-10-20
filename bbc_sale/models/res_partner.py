# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    amount_free_shipping = fields.Float(
        'Free shipping from',
        help=('The amount from which purchase orders are shipped out free '
              'from this supplier'))
    pos_order_count = fields.Integer(
        compute='_pos_order_count', string='# of POS Orders')

    @api.multi
    def _pos_order_count(self):
        for partner in self:
            partner.pos_order_count = len(
                self.env['pos.order'].search(
                    [('partner_id', '=', partner.id)]))

    @api.model
    def _commercial_fields(self):
        res = super(Partner, self)._commercial_fields()
        res.append('amount_free_shipping')
        return res
