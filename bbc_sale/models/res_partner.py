# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    amount_free_shipping = fields.Float('Free shipping from')

    @api.model
    def _commercial_fields(self):
        res = super(Partner, self)._commercial_fields()
        res.append('amount_free_shipping')
        return res
