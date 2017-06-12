# coding: utf-8
from openerp.tests.common import TransactionCase


class TestConsuSingleAttr(TransactionCase):
    def test_consu_single_attr(self):
        product = self.env['product.product'].create({
            'name': 'bbc_sale_consu_product',
            'type': 'consu'})
        attr1 = self.env['product.attribute'].create({
            'name': 'Attribute1',
            'value_ids': [(0, 0, {
                'name': 'Attr1 - Val1'})],
        })
        attr2 = self.env['product.attribute'].create({
            'name': 'Attribute2',
            'value_ids': [(0, 0, {
                'name': 'Attr2 - Val1'})],
        })

        self.assertFalse(product.consu_single_attr)
        product.write({'attribute_value_ids': [(4, attr1.value_ids.id)]})
        self.assertTrue(product.consu_single_attr)
        product.write({'attribute_value_ids': [(4, attr2.value_ids.id)]})
        self.assertFalse(product.consu_single_attr)
        product.write({'attribute_value_ids': [(3, attr2.value_ids.id)]})
        self.assertTrue(product.consu_single_attr)
        product.write({'type': 'product'})
        self.assertFalse(product.consu_single_attr)
