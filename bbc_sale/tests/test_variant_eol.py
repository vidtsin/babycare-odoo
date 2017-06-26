# coding: utf-8
from openerp.tests.common import TransactionCase


class TestVariantEOL(TransactionCase):
    def setUp(self):
        super(TestVariantEOL, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'bbc_sale_test',
            'type': 'product'})
        self.template = self.product.product_tmpl_id
        self.bom_product = self.env['product.product'].create({
            'name': 'bbc_sale_bom_product',
            'type': 'consu'})
        self.component = self.env['product.product'].create({
            'name': 'bbc_sale_component'})
        self.bom = self.env['mrp.bom'].create({
            'name': 'Test BOM',
            'product_id': self.bom_product.id,
            'product_tmpl_id': self.bom_product.product_tmpl_id.id,
            'product_uom': self.env.ref('product.product_uom_unit').id,
            'product_qty': 1,
            'type': 'phantom',
            'bom_line_ids': [
                (0, 0, {
                    'product_id': self.component.id,
                    'product_uom': self.env.ref('product.product_uom_unit').id,
                }),
            ]})

    def test_01_state_to_variant_eol(self):
        self.assertEqual(self.product.variant_eol, False)
        self.product.product_tmpl_id.write({'state': 'end'})
        self.assertEqual(self.product.variant_eol, True)
        self.product.product_tmpl_id.write({'state': 'sellable'})
        self.assertEqual(self.product.variant_eol, False)
        self.product.product_tmpl_id.write({'state': 'end'})
        self.assertEqual(self.product.variant_eol, True)

    def test_02_variant_eol_to_state(self):
        self.product.write({'state': 'sellable'})
        self.product.copy({'product_tmpl_id': self.template.id})
        self.assertEqual(len(self.template.product_variant_ids), 2)
        variants = self.template.product_variant_ids
        variants[0].write({'variant_eol': True})
        self.assertEqual(self.product.state, 'sellable')
        variants[1].write({'variant_eol': True})
        self.assertEqual(self.product.state, 'end')

    def test_03_bom_component_eol(self):
        self.assertFalse(self.bom_product.variant_eol)
        self.bom_product.update_availability()
        self.assertTrue(self.bom_product.variant_published)

        self.component.write({'variant_eol': True})
        self.assertTrue(self.bom_product.variant_eol)

        self.component.write({'variant_eol': False})
        self.assertFalse(self.bom_product.variant_eol)

        self.component.write({'variant_eol': True})
        self.assertEqual(self.bom_product.state, 'end')
        self.bom_product.update_availability()
        self.assertFalse(self.bom_product.variant_published)

        self.env.cr.execute(
            """ UPDATE product_product
            SET write_date = '2017-01-01'
            """)
        self.env['product.template'].deactivate_obsolete_products()
        self.assertTrue(self.bom_product.active)

        self.bom.unlink()
        self.env['product.template'].deactivate_obsolete_products()
        self.assertFalse(self.bom_product.active)
