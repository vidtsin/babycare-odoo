# coding: utf-8
from openerp.fields import Date
from openerp.addons.stock.tests.common import TestStockCommon


class TestBarcodeNoConsuSingleAttr(TestStockCommon):
    def setUp(self):
        super(TestBarcodeNoConsuSingleAttr, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'bbc_stock_bom_product',
            'type': 'consu',
            'default_code': 'product_barcode'})
        self.attr = self.env['product.attribute'].create({
            'name': 'Attribute1',
            'value_ids': [(0, 0, {
                'name': 'Attr1 - Val1'})],
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

    def test_01_barcode_no_consu_single_attr(self):
        """ Products that are not consu/single attr are processed as usual """
        self.assertFalse(self.product.consu_single_attr)
        self.assertTrue(
            self.picking.process_barcode_from_ui(
                self.picking.id, 'product_barcode', [])['operation_id'])

    def test_02_barcode_consu_single_attr(self):
        """ Consumables with a single attribute are ignored """
        self.product.write({
            'attribute_value_ids': [(4, self.attr.value_ids.id)]})
        self.assertTrue(self.product.consu_single_attr)
        self.assertFalse(
            self.picking.process_barcode_from_ui(
                self.picking.id, 'product_barcode', [])['operation_id'])
