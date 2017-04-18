# coding: utf-8
from openerp import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'
    product_id = fields.Many2one(domain=[('type', '!=', 'consu')])
