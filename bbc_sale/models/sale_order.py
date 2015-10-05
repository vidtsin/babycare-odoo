from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    remarks = fields.Char()

    @api.multi
    def action_ship_create(self):
        """
        Populate the manual field that registers if the picking's sale order
        has been paid. Additionally, this happens in a custom server action.
        """
        res = super(SaleOrder, self).action_ship_create()
        for sale_order in self:
            if sale_order.invoiced:
                sale_order.picking_ids.write({'x_is_paid': True})
        return res
