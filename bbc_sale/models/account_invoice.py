from openerp import models, api
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class Invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def confirm_paid(self):
        """
        If an invoice gets paid of a sale order in shipment exception,
        regenerate the picking. This covers the use case where the customer
        pays after the shipping was cancelled manually after the due date
        had already passed.
        """
        res = super(Invoice, self).confirm_paid()
        self.env['sale.order'].search(
            [('invoice_ids', 'in', self.ids),
             ('state', '=', 'shipping_except')]
        ).signal_workflow('ship_recreate')
        return res

    @api.multi
    def action_move_create(self):
        if self.type.startswith('in_') and not self.supplier_invoice_number:
            raise UserError(_(
                'Please enter a supplier invoice number first'))
        return super(Invoice, self).action_move_create()
