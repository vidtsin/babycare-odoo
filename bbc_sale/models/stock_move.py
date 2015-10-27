# -*- coding: utf-8 -*-
from openerp import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    product_state = fields.Selection(
        related='product_id.state')
    virtual_available = fields.Float(
        related='product_id.virtual_available')
