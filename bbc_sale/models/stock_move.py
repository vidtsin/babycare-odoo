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
        """ The set of move ids can be changed by phantom boms """
        move_ids = super(StockMove, self).action_confirm()
        self.browse(move_ids).mapped('product_id').update_availability()
        return move_ids

    @api.multi
    def action_cancel(self):
        res = super(StockMove, self).action_cancel()
        self.mapped('product_id').update_availability()
        return res

    @api.multi
    def action_done(self):
        res = super(StockMove, self).action_done()
        self.mapped('product_id').update_availability()
        return res
