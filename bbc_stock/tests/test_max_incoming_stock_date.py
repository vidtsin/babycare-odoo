# coding: utf-8
from openerp.fields import Date
from openerp.addons.stock.tests.common import TestStockCommon
from datetime import timedelta


class TestMaxDate(TestStockCommon):
    def setUp(self):
        super(TestMaxDate, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'test max date',
            'type': 'product',
        })
        self.seller_delay = 5
        self.env['product.supplierinfo'].create({
            'name': self.partner_delta_id,
            'delay': self.seller_delay,
            'product_tmpl_id': self.product.product_tmpl_id.id,
        })
        self.bom_product = self.env['product.product'].create({
            'name': 'test max date bom',
            'type': 'consu',
        })
        self.env['mrp.bom'].create({
            'product_id': self.bom_product.id,
            'product_tmpl_id': self.bom_product.product_tmpl_id.id,
            'bom_line_ids': [(0, 0, {
                'product_id': self.product.id})],
        })
        self.today = Date.context_today(self.env.user)

    def test_01_max_date(self):
        next_year = '%s-01-01' % (int(self.today[:4]) + 1)
        next_year_feb = '%s-02-01' % (int(self.today[:4]) + 1)
        next_year_feb6 = '%s-02-06' % (int(self.today[:4]) + 1)

        delay = Date.to_string(
            Date.from_string(self.today) + timedelta(days=self.seller_delay))
        self.assertEqual(
            self.product.max_incoming_stock_date, delay)
        self.product.max_incoming_stock_date_override = True
        self.product.max_incoming_stock_date_override_value = next_year
        self.assertEqual(
            self.product.max_incoming_stock_date, next_year)
        self.assertEqual(
            self.bom_product.max_incoming_stock_date, next_year)
        self.product.max_incoming_stock_date_override = False
        picking_in = self.PickingObj.create({
            'partner_id': self.partner_delta_id,
            'picking_type_id': self.picking_type_in})
        self.MoveObj.create({
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'picking_id': picking_in.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.stock_location,
            'date_expected': next_year_feb,
        })
        picking_in.action_confirm()
        self.assertEqual(self.product.max_incoming_stock_date, next_year_feb)
        self.assertEqual(
            self.bom_product.max_incoming_stock_date, next_year_feb)

        self.product.max_incoming_stock_date_override = True
        self.product.max_incoming_stock_date_override_value = self.today
        self.assertEqual(self.product.max_incoming_stock_date, self.today)
        self.env['product.product'].reset_max_incoming_date_override()
        self.assertEqual(self.product.max_incoming_stock_date, next_year_feb)

        # When a product has to be ordered, add supplier lead time to max date
        # expected of running orders
        picking_out = self.PickingObj.create({
            'partner_id': self.partner_delta_id,
            'picking_type_id': self.picking_type_out})
        move = self.MoveObj.create({
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'picking_id': picking_out.id,
            'location_dest_id': self.customer_location,
            'location_id': self.stock_location,
            'date_expected': next_year,
        })
        picking_out.action_confirm()
        self.product.refresh()
        self.assertEqual(self.product.max_incoming_stock_date, next_year_feb6)

        # Test that we can modify the picking's max_date (#2800)
        # Call _register_hook manually because tests run before Odoo does
        self.env['stock.picking']._register_hook()
        picking_out.write({'max_date': next_year_feb6})
        self.assertEqual(move.date_expected, next_year_feb6 + ' 00:00:00')
        self.assertEqual(picking_out.max_date, next_year_feb6 + ' 00:00:00')
