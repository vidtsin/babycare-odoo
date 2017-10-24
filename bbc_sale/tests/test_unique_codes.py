# coding: utf-8
from openerp.exceptions import ValidationError
from openerp.tests.common import TransactionCase
from openerp.tools.misc import mute_logger


class TestUniqueCodes(TransactionCase):
    def _configurable(self):
        product = self.env['product.product'].create({
            'name': 'bbc_sale_bom_product',
            'type': 'consu',
            'default_code': '__test_unique_code',
            'ean13': '1122334455666',
        })

        self.env['mrp.bom'].create({
            'name': 'Test BOM',
            'product_id': product.id,
            'product_tmpl_id': product.product_tmpl_id.id,
            'product_uom': self.env.ref('product.product_uom_unit').id,
            'product_qty': 1,
            'type': 'phantom',
        })
        attribute = self.env['product.attribute'].create({'name': 'Color'})
        self.env['product.attribute.line'].create({
            'attribute_id': attribute.id,
            'product_tmpl_id': product.product_tmpl_id.id,
        })

        return product

    def test_unique_codes(self):
        product = self.env['product.product'].create({
            'name': 'bbc_sale_test_product',
            'type': 'consu',
            'default_code': '__test_unique_code',
            'ean13': '1122334455666',
        })
        product2 = product.copy()
        with self.assertRaisesRegexp(ValidationError, '__test_unique_code'):
            with mute_logger('openerp.models'):
                product2.write({'default_code': '__test_unique_code'})

        product3 = product.copy()
        with self.assertRaisesRegexp(ValidationError, '1122334455666'):
            with mute_logger('openerp.models'):
                product3.write({'ean13': '1122334455666'})

    def test_unique_codes_configurable(self):
        product = self._configurable()
        self.assertTrue(product.configurable)
        new_product = product.copy()
        new_product.write({'default_code': '__test_unique_code'})
        new_product.write({'ean13': '1122334455666'})
