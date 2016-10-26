# coding: utf-8
from openerp import api, models


class Inventory(models.Model):
    _inherit = 'stock.inventory'

    @api.model
    def post_inventory(self, inv):
        res = super(Inventory, self).post_inventory()
        self.browse(inv.id).mapped('product_id').update_availability()
        return res

    @api.multi
    def action_cancel_draft(self, cr, uid, ids, context=None):
        res = super(Inventory, self).action_cancel_draft()
        self.mapped('product_id').update_availability()
        return res
