from openerp.tests.common import TransactionCase


class TestProductTranslations(TransactionCase):
    def setUp(self):
        super(TestProductTranslations, self).setUp()
        self.prod_obj = self.env['product.product'].with_context(lang='nl_NL')
        self.product = self.prod_obj.create({'name': 'Testprodukt'})

    def test_01_product_translation(self):
        product = self.product.copy()
        product.write({'name': 'New name'})
        self.assertEqual(
            product.with_context(lang='en_US').name, 'New name')

    def test_02_product_translation(self):
        product = self.product.copy()
        self.assertEqual(
            product.with_context(lang='en_US').name, '/')

    def test_04_template_translation(self):
        template = self.product.product_tmpl_id.copy()
        self.assertEqual(
            template.with_context(lang='en_US').name, '/')
        template.write({'name': 'New name'})
        self.env.invalidate_all()
        self.assertEqual(
            template.with_context(lang='en_US').name, 'New name')
        self.assertEqual(template.product_variant_ids[0].name, 'New name')
        self.assertEqual(
            template.with_context(lang='en_US').product_variant_ids[0].name,
            'New name')
