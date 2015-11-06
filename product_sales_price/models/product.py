# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class Product(models.Model):
    _inherit = 'product.product'

    default_sale_price = fields.Float(
        'Default sales price',
        compute="_get_default_sale_price",
        digits_compute=dp.get_precision('Product Price'))

    @api.multi
    def _get_default_sale_price(self):
        """ Cf. _product_template_price from addons/product/product.py.
        Do not want to modify this upstream function for fear of side effects.
        """
        pricelist = False
        self.env.cr.execute(
            """
            SELECT COALESCE(
                (SELECT value_reference FROM ir_property
                     WHERE name = 'property_product_pricelist'
                         AND res_id IS NULL
                         AND company_id = %s),
                (SELECT value_reference FROM ir_property
                     WHERE name = 'property_product_pricelist'
                         AND res_id IS NULL
                         AND company_id IS NULL))
            """, (self.env.user.company_id.id,))
        row = self.env.cr.fetchone()
        if row:
            pricelist = self.env['product.pricelist'].browse(
                int(row[0][row[0].rfind(',') + 1:]))
        for product in self:
            if not pricelist:
                product.default_sale_price = 0.0
            else:
                product.default_sale_price = pricelist.price_get(
                    product.id, 1.0)[pricelist.id]


class Template(models.Model):
    _inherit = 'product.template'

    default_sale_price = fields.Float(
        'Default sales price',
        compute="_get_default_sale_price",
        digits_compute=dp.get_precision('Product Price'))

    @api.multi
    def _get_default_sale_price(self):
        for template in self:
            if not self.product_variant_ids:
                self.default_sale_price = 0.0
                continue
            self.default_sale_price = (
                self.product_variant_ids[0].default_sale_price)
