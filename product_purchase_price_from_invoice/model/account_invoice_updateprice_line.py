# coding: utf-8
# Copyright (C) 2014 Therp BV <http://therp.nl>.
#           (C) 2017 Opener B.V. <https://opener.am>
# @author Stefan Rijnhart <stefan@opener.am>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import api, fields, models
from openerp.addons import decimal_precision as dp
from openerp.tools.float_utils import float_round
from openerp.tools.translate import _


class UpdatePriceLine(models.TransientModel):
    _name = 'account.invoice.updateprice.line'
    _description = 'Update price wizard line'

    updateprice_id = fields.Many2one('account.invoice.updateprice')
    update = fields.Boolean(default=True)
    product = fields.Many2one('product.product', readonly=True)
    current_cost_price = fields.Float(
        digits=dp.get_precision('Product Price'),
        readonly=True)
    price_on_invoice = fields.Float(
        digits=dp.get_precision('Product Price'),
        readonly=True)
    standard_margin_rate = fields.Float(
        string='Margin %',
        digits=dp.get_precision('Product Price'))
    current_sale_price = fields.Float(
        digits=dp.get_precision('Product Price'),
        readonly=True)
    new_sale_price = fields.Float(
        digits=dp.get_precision('Product Price'))

    @api.onchange('new_sale_price')
    def _onchange_new_sale_price(self):
        price_vat_excl = self.product.taxes_id.compute_all(
            self.new_sale_price, 1, product=self.product.id)['total']
        if not price_vat_excl:
            self.standard_margin_rate = 999
        else:
            self.standard_margin_rate = (
                price_vat_excl - self.price_on_invoice) / price_vat_excl * 100

    @api.onchange('standard_margin_rate')
    def _onchange_standard_margin_rate(self):
        if self.standard_margin_rate >= 100:
            return
        price_vat_excl = 100 * (
            self.price_on_invoice / (100 - self.standard_margin_rate))
        tax = self.product.taxes_id
        if tax:
            if tax.type != 'percent':
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _(
                            'Tax of type %s is not supported') % tax.type}}
            if tax.child_ids:
                return {
                    'warning': {
                        'title': _('Warning'),
                        'message': _(
                            'Tax with child ids is not supported')}}
            sale_price = price_vat_excl + float_round(
                price_vat_excl * tax.amount,
                self.env['decimal.precision'].precision_get('Account'))
        else:
            sale_price = price_vat_excl
        sale_price = price_vat_excl + float_round(
            price_vat_excl * tax.amount,
            self.env['decimal.precision'].precision_get('Account'))
        # Allow for rounding difference due to tax calculation
        if abs(
            float_round(
                self.new_sale_price - sale_price,
                self.env['decimal.precision'].precision_get('Account')
                )) > 0.01:
            self.new_sale_price = sale_price
