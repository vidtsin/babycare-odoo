from openerp import models, fields, api


class Picking(models.Model):
    _inherit = 'stock.picking'

    remarks = fields.Char(compute='get_remarks')

    @api.depends('move_lines')
    @api.one
    def get_remarks(self):
        purchases = self.move_lines.mapped('purchase_line_id.order_id')
        sales = self.env['sale.order'].search(
            [('procurement_group_id', 'in', self.mapped('group_id').ids),
             ('remarks', '!=', False),
             ('remarks', '!=', '')])
        self.remarks = '; '.join(
            [purchase.remarks for purchase in purchases] +
            [sale.remarks for sale in sales])
