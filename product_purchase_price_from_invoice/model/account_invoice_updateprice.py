# coding: utf-8
# Copyright (C) 2014 Therp BV <http://therp.nl>.
#           (C) 2017 Opener B.V. <https://opener.am>
# @author Stefan Rijnhart <stefan@opener.am>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models


class UpdatePrice(models.TransientModel):
    _name = 'account.invoice.updateprice'
    _description = 'Update Prices on this invoice'

    name = fields.Char()
    line_ids = fields.One2many(
        'account.invoice.updateprice.line', 'updateprice_id')

    @api.multi
    def save_new_prices(self):
        self.ensure_one()
        for line in self.line_ids:
            if not line.update:
                continue
            line.product.write({
                'standard_price': line.price_on_invoice,
                'lst_price': line.new_sale_price,
            })
