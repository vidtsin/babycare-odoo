# coding: utf-8
# Copyright (C) 2014 Therp BV <http://therp.nl>.
#           (C) 2017 Opener B.V. <https://opener.am>
# @author Stefan Rijnhart <stefan@opener.am>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# coding: utf-8
from openerp import api, models


class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def _prepare_update_price_wizard_line(self, wizard):
        """
        Return a set of create values for a line in the wizard.

        :param line: invoice line browse record
        """
        self.ensure_one()
        if not self.product_id:
            return

        if self.uos_id != self.product_id.uom_id:
            # Not implemented
            return

        currency = self.env.user.company_id.currency_id
        if currency.is_zero(
                self.product_id.standard_price - self.price_unit):
            # Price has not changed
            return

        ex_vat = self.product_id.list_price_vat_excl
        if ex_vat:
            rate = (ex_vat - self.price_unit) / ex_vat * 100
        else:
            rate = 999

        return {
            'updateprice_id': wizard.id,
            'product': self.product_id.id,
            'current_cost_price': self.product_id.standard_price,
            'price_on_invoice': self.price_unit,
            'current_sale_price': self.product_id.lst_price,
            'new_sale_price': self.product_id.lst_price,
            'standard_margin_rate': rate,
            'standard_margin': ex_vat - self.price_unit,
        }
