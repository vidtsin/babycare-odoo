# coding: utf-8
from openerp.tests.common import TransactionCase
from openerp.fields import Date


class TestSalesPrice(TransactionCase):
    def setUp(self):
        super(TestSalesPrice, self).setUp()
        attribute = self.env['product.attribute'].create({
            'name': 'sales_price_attribute',
        })
        self.red = self.env['product.attribute.value'].create({
            'name': 'red',
            'attribute_id': attribute.id,
        })
        self.blue = self.env['product.attribute.value'].create({
            'name': 'blue',
            'attribute_id': attribute.id,
        })

        # Product is created with a list price of 75.95
        self.template = self.env['product.template'].create({
            'name': 'bbc_stock_bom_product',
            'type': 'product',
            'list_price': 75.95,
            'attribute_line_ids': [(
                0, 0, {
                    'attribute_id': attribute.id,
                    'value_ids': [(6, 0, attribute.value_ids.ids)],
                })],
        })
        self.env['product.attribute.price'].create({
            'product_tmpl_id': self.template.id,
            'value_id': self.blue.id,
            'price_extra': -20,
        })
        self.today = Date.context_today(self.env.user)
        self.pricelist_version = self.env['product.pricelist.version'].search([
            '|', ('date_start', '=', False), ('date_start', '<=', self.today),
            '|', ('date_end', '=', False), ('date_end', '>=', self.today),
            ('pricelist_id.type', '=', 'sale')], limit=1)
        self.pricelist = self.pricelist_version.pricelist_id

    def test_sales_price_special(self):
        """ Sales price for a variant with attribute price plus fixed price
        """
        # Set a default special price of 29.95 for variants of this template
        self.env['product.pricelist.item'].create({
            'price_version_id': self.pricelist_version.id,
            'base': self.env.ref('product.list_price').id,
            'product_tmpl_id': self.template.id,
            'price_discount': -1,
            'price_surcharge': 29.95,
        })
        self.assertEqual(self.red.product_ids.default_sale_price, 29.95)

        # Problem: the fixed pricelist item ignores the attribute price
        self.assertEqual(
            self.pricelist.price_get(
                self.blue.product_ids.id, 1.0)[self.pricelist.id], 29.95)

        # This is reflected in the computation of the sales price
        self.assertEqual(self.blue.product_ids.default_sale_price, 29.95)

    def test_sales_price_no_special(self):
        """ Sales price for a variant with attribute price but no pricelist item
        """
        self.assertEqual(self.red.product_ids.default_sale_price, 75.95)

        # on products without a fixed pricelist item, the attribute price is
        # included correctly
        self.assertEqual(
            self.pricelist.price_get(
                self.blue.product_ids.id, 1.0)[self.pricelist.id], 55.95)

        # The attribute price is included correcly by the
        # custom computation of the sales price as well
        self.assertEqual(self.blue.product_ids.default_sale_price, 55.95)
