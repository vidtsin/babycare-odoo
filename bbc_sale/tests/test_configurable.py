# coding: utf-8
from openerp.tests.common import TransactionCase


class TestConfigurable(TransactionCase):
    def test_configurable(self):
        template = self.env['product.template'].create({
            'name': 'bbc_sale_bom_product',
            'type': 'consu'})

        def create_bom():
            return self.env['mrp.bom'].create({
                'name': 'Test BOM',
                'product_id': template.product_variant_ids[0].id,
                'product_tmpl_id': template.id,
                'product_uom': self.env.ref('product.product_uom_unit').id,
                'product_qty': 1,
                'type': 'phantom',
            })

        self.assertFalse(template.configurable)

        bom = create_bom()
        self.assertFalse(template.configurable)

        attribute = self.env['product.attribute'].create({'name': 'Color'})
        self.env['product.attribute.line'].create({
            'attribute_id': attribute.id,
            'product_tmpl_id': template.id,
        })
        self.assertTrue(template.configurable)

        template.write({'type': 'service'})
        self.assertFalse(template.configurable)
        template.write({'type': 'consu'})
        self.assertTrue(template.configurable)

        bom.unlink()
        self.assertFalse(template.configurable)
        create_bom()
        self.assertTrue(template.configurable)
