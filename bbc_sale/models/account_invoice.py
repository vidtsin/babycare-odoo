from openerp import models, api


class Invoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def confirm_paid(self):
        """
        If an invoice gets paid of a sale order in shipment exception,
        regenerate the picking. This covers the use case where the customer
        pays after the shipping was cancelled manually after the due date
        had already passed.

        Populate the manual field that registers if the picking's sale order
        has been paid. For regular pickings, this happens in a custom server
        action.
        """
        res = super(Invoice, self).confirm_paid()
        self.env['sale.order'].search(
            [('invoice_ids', 'in', self.ids),
             ('state', '=', 'shipping_except')]
        ).signal_workflow('ship_recreate')
        return res
