# coding: utf-8
from openerp.tests.common import TransactionCase


class TestConfigurable(TransactionCase):
    def test_configurable(self):
        product = self.env['product.product'].create({
            'name': 'bbc_sale_bom_product',
            'type': 'consu'})

        def create_bom():
            return self.env['mrp.bom'].create({
                'name': 'Test BOM',
                'product_id': product.id,
                'product_tmpl_id': product.product_tmpl_id.id,
                'product_uom': self.env.ref('product.product_uom_unit').id,
                'product_qty': 1,
                'type': 'phantom',
            })

        self.assertFalse(product.configurable)
        bom = create_bom()
        self.assertFalse(product.configurable)
        product2 = product.copy(
            default={'product_tmpl_id': product.product_tmpl_id.id})
        self.assertTrue(product2.configurable)

        product.write({'type': 'service'})
        self.assertFalse(product.configurable)
        product.write({'type': 'consu'})
        self.assertTrue(product2.configurable)

        bom.unlink()
        self.assertFalse(product.configurable)
        create_bom()
        self.assertTrue(product2.configurable)
