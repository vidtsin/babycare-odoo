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
    def action_confirm(self):
        res = super(Picking, self).action_confirm()
        self.update_product_availability()
        return res

    @api.multi
    def action_cancel(self):
        res = super(Picking, self).action_cancel()
        self.update_product_availability()
        return res

    @api.multi
    def do_transfer(self):
        res = super(Picking, self).do_transfer()
        self.update_product_availability()
        return res

    @api.multi
    def update_product_availability(self):
        self.mapped('move_lines.product_id').update_availability()
