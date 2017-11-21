# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class CustomOption(models.Model):
    _name = 'custom.option'

    option_type = fields.Selection(
        [
            ('buggies.agecategory', 'buggies.agecategory'),
            ('buggies.maxcarryweight', 'buggies.maxcarryweight'),
            ('buggies.numberofwheels', 'buggies.numberofwheels'),
            ('carriers.directionofuse', 'carriers.directionofuse'),
            ('carriers.maxcarryweight', 'carriers.maxcarryweight'),
            ('carriers.type', 'carriers.type'),
            ('carseats.agecategory', 'carseats.agecategory'),
            ('carseats.childlength', 'carseats.childlength'),
            ('carseats.childweight', 'carseats.childweight'),
            ('carseats.directionofuse', 'carseats.directionofuse'),
            ('carseats.installmethod', 'carseats.installmethod'),
            ('clothes.season', 'clothes.season'),
            ('clothes.size', 'clothes.size'),
            ('color', 'color'),
            ('highchairs.agecategory', 'highchairs.agecategory'),
            ('highchairs.material', 'highchairs.material'),
            ('monitors.maxrange', 'monitors.maxrange'),
            ('rockers.maxcarryweight', 'rockers.maxcarryweight'),
            ('strollers.numberofwheels', 'strollers.numberofwheels'),
            ('textiles.size', 'textiles.size'),
            ('toys.agecategory', 'toys.agecategory'),
            ('toys.type', 'toys.type'),
            ('warranty', 'warranty'),
        ], required=True)
    mageId = fields.Integer('Magento Option Id')
    name = fields.Char('Value', required=True, translate=True)
    synced = fields.Boolean('Synced?', default=False)

    @api.one
    def unlink(self):
        option_type = self.option_type
        mage_option_type = option_type.replace('.', '_')
        option_type_id = ('product_%s_id' % mage_option_type)
        product_ids = self.env['product.product'].search(
            [(option_type_id, 'in', self.ids)]
        )
        if product_ids:
            raise UserError(
                (
                    'The operation cannot be completed:\n'
                    'You trying to delete a record with'
                    ' a reference on a product variant.'
                )
            )
        return super(CustomOption, self).unlink()

    _sql_constraints = [
        (
            'name_unique',
            'UNIQUE(option_type, name)',
            "The name of the record must be unique"
        )
    ]
