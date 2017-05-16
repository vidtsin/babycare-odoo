# coding: utf-8
from openerp.tests.common import TransactionCase
from openerp.fields import Date


class TestFiscalPosition(TransactionCase):

    def create_partner(self, country_code):
        return self.env['res.partner'].create({
            'name': 'TestPartnerBabycareSale%s' % country_code,
            'country_id': self.env.ref('base.%s' % country_code).id,
        })

    def setUp(self):
        super(TestFiscalPosition, self).setUp()
        self.partner_nl = self.create_partner('nl')
        self.partner_eu = self.create_partner('fr')
        self.partner_world = self.create_partner('us')

    def create_order(self, partner, shipping):
        return self.env['sale.order'].create({
            'partner_id': partner.id,
            'partner_invoice_id': partner.id,
            'partner_shipping_id': shipping.id,
            'user_id': self.env.user.id,
            'pricelist_id': partner.property_product_pricelist.id,
            'date_order': Date.context_today(self.env.user),
        })

    def test_create(self):
        self.assertEqual(
            self.create_order(
                self.partner_eu, self.partner_nl).fiscal_position,
            self.env.ref('bbc_sale.fispos_nl'))
        self.assertEqual(
            self.create_order(
                self.partner_world, self.partner_eu).fiscal_position,
            self.env.ref('bbc_sale.fispos_eu'))
        self.assertEqual(
            self.create_order(
                self.partner_nl, self.partner_eu).fiscal_position,
            self.env.ref('bbc_sale.fispos_eu'))

    def test_onchange(self):
        res = self.env['sale.order'].onchange_delivery_id(
            self.env.user.company_id.id, self.partner_nl.id,
            self.partner_eu.id, False)
        self.assertEqual(
            res['value']['fiscal_position'],
            self.env.ref('bbc_sale.fispos_eu').id)

        res = self.env['sale.order'].onchange_delivery_id(
            self.env.user.company_id.id, self.partner_eu.id,
            self.partner_nl.id, False)
        self.assertEqual(
            res['value']['fiscal_position'],
            self.env.ref('bbc_sale.fispos_nl').id)

        res = self.env['sale.order'].onchange_delivery_id(
            self.env.user.company_id.id, self.partner_nl.id,
            self.partner_world.id, False)
        self.assertEqual(
            res['value']['fiscal_position'],
            self.env.ref('bbc_sale.fispos_world').id)
