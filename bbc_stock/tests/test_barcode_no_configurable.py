# coding: utf-8
from openerp.fields import Date
from openerp.addons.stock.tests.common import TestStockCommon


class TestBarcodeNoConfigurable(TestStockCommon):
    def setUp(self):
        super(TestBarcodeNoConfigurable, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'bbc_stock_bom_product',
            'type': 'consu',
            'default_code': 'product_barcode'})

        self.env['mrp.bom'].create({
            'name': 'Test BOM',
            'product_id': self.product.id,
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_uom': self.env.ref('product.product_uom_unit').id,
            'product_qty': 1,
            'type': 'phantom',
        })

        self.picking = self.PickingObj.create({
            'partner_id': self.partner_delta_id,
            'picking_type_id': self.picking_type_in})
        self.MoveObj.create({
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom_qty': 1,
            'product_uom': self.product.uom_id.id,
            'picking_id': self.picking.id,
            'location_id': self.supplier_location,
            'location_dest_id': self.stock_location,
            'date_expected': Date.context_today(self.env.user),
        })
        self.picking.action_confirm()

    def test_01_barcode_no_configurable(self):
        """ Non-configurable products are processed as usual """
        self.assertFalse(self.product.configurable)
        self.assertTrue(
            self.picking.process_barcode_from_ui(
                self.picking.id, 'product_barcode', [])['operation_id'])

    def test_02_barcode_configurable(self):
        """ Configurable products are ignored """
        self.product.copy(
            default={'product_tmpl_id': self.product.product_tmpl_id.id})
        self.assertTrue(self.product.configurable)
        self.assertFalse(
            self.picking.process_barcode_from_ui(
                self.picking.id, 'product_barcode', [])['operation_id'])
