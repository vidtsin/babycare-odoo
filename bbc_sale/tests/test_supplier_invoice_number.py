from openerp.tests.common import TransactionCase
from openerp.exceptions import Warning as UserError


class TestSupplierInvoiceNumber(TransactionCase):
    def setUp(self):
        super(TestSupplierInvoiceNumber, self).setUp()
        partner = self.env['res.partner'].search(
            [('supplier', '=', True)], limit=1) or self.env[
                'res.partner'].create({
                    'name': 'Test',
                    'supplier': True,
                })

        vals = {
            'type': 'in_invoice',
            'partner_id': partner.id,
            'invoice_line': [(0, 0, {
                'name': 'Test',
                'price_unit': 1.0,
                'quantity': 1.0,
            })],
        }
        vals.update(self.env['account.invoice'].onchange_partner_id(
            'in_invoice', partner.id,
            company_id=self.env.user.company_id.id)['value'])
        self.invoice = self.env['account.invoice'].create(vals)

    def test_01_raises(self):
        with self.assertRaises(UserError):
            self.invoice.signal_workflow('invoice_open')

    def test_02_success(self):
        # Split up tests because workflow sql operations cause inconsistencies
        # before rollback
        self.invoice.write({'supplier_invoice_number': '1'})
        self.invoice.signal_workflow('invoice_open')
        self.assertEqual(self.invoice.state, 'open')
