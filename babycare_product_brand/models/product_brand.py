# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class ProductBrand(models.Model):
    _inherit = 'product.brand'
    name = fields.Char(translate=True)

    @api.multi
    def unlink(self):
        product_ids = self.env['product.product'].search([(
            'product_brand_id', 'in', self.ids
        )])
        if product_ids:
            raise UserError(
                ('The operation cannot be completed:'
                 '\nYou trying to delete a product brand with'
                 'a reference on a product variant.')
            )
        return super(ProductBrand, self).unlink()

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(name)',
            "The Name of the Product Brand must be unique"
        )
    ]
