# -*- coding: utf-8 -*-
from openerp import api, models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_state = fields.Selection(
        related='product_id.state')
    virtual_available = fields.Float(
        related='product_id.virtual_available')

    @api.multi
    def action_confirm(self):
        res = super(StockMove, self).action_confirm()
        self.mapped('product_id').update_availability()
        return res

    @api.multi
    def action_cancel(self):
        res = super(StockMove, self).action_cancel()
        self.mapped('product_id').update_availability()
        return res

    @api.multi
    def action_done(self):
        res = super(StockMove, self).action_cancel()
        self.mapped('product_id').update_availability()
        return res
