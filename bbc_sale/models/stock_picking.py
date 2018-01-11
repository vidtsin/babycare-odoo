# coding: utf-8
from openerp import models, fields, api


class Picking(models.Model):
    _inherit = 'stock.picking'

    remarks = fields.Char(string='Remarks', compute='get_remarks')
    purchase_id = fields.Many2one(
        'purchase.order', string='Purchase order',
        help='First of any related purchase orders in the system',
        compute='_get_purchase_id')

    @api.multi
    def _get_purchase_id(self):
        # Get the first of any related purchase orders
        for picking in self:
            for move in picking.move_lines:
                if move.purchase_line_id:
                    picking.purchase_id = move.purchase_line_id.order_id
                    break

    @api.depends('move_lines')
    @api.one
    def get_remarks(self):
        purchases = self.move_lines.mapped('purchase_line_id.order_id')
        sales = self.env['sale.order'].search(
            [('procurement_group_id', 'in', self.mapped('group_id').ids),
             ('remarks', '!=', False),
             ('remarks', '!=', '')])
        self.remarks = '; '.join(
            [purchase.remarks for purchase in purchases if purchase.remarks] +
            [sale.remarks for sale in sales])

    @api.multi
    def send_mail_outgoing_delivery(self):
        """ Runs the server action of sending an email with the template
        Magento | Send Email After Outgoing Delivery Is Shipped.
        active_ids included in context because the server action has to
        work in the Barcode Scanning Interface as well. """
        template = self.env.ref(
            'bbc_sale.action_send_email_delivery_shipped_magento')
        self.env['ir.actions.server'].browse(template.id).with_context(
            active_ids=self.ids).run()

    @api.multi
    def do_transfer(self):
        """ Trigger send_mail_outgoing_delivery on transfer of outgoing
        delivery to automatically send an email to the customer. """
        res = super(Picking, self).do_transfer()
        self.send_mail_outgoing_delivery()
        return res
