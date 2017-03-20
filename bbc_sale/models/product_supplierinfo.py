# coding: utf-8
from openerp import api, models


class Supplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    @api.onchange('name')
    def onchange_seller(self):
        """ Set default delay when a supplier is chosen """
        partner = self.name.commercial_partner_id
        if partner.default_delay:
            self.delay = partner.default_delay

    @api.model
    def create(self, vals):
        """ Set default delay if this is a product import """
        res = super(Supplierinfo, self).create(vals)
        partner = res.name.commercial_partner_id
        if not vals.get('delay') and self.env.context.get(
                'set_seller_default_delay') and partner.default_delay:
            res.write({'delay': partner.default_delay})
        return res
