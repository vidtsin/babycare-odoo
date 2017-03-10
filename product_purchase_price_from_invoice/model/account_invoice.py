# coding: utf-8
# Copyright (C) 2014 Therp BV <http://therp.nl>.
#           (C) 2017 Opener B.V. <https://opener.am>
# @author Stefan Rijnhart <stefan@opener.am>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# coding: utf-8
from openerp import api, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class Invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def price_update_wizard(self):
        """
        Create a wizard and lines on the wizard for all invoice
        lines of this invoice with a product on them.
        """
        self.ensure_one()
        wizard = self.env['account.invoice.updateprice'].create({})
        for line in self.invoice_line:
            if not line.product_id:
                continue
            vals = line._prepare_update_price_wizard_line(wizard)
            if vals is None:
                continue
            self.env['account.invoice.updateprice.line'].create(vals)

        if not wizard.line_ids:
            raise UserError(
                _('No product found with a deviating cost price'))

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': wizard._name,
            'target': 'new',
            'res_id': wizard.id,
        }
