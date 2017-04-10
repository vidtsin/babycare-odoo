# coding: utf-8
from openerp import fields, models


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'
    picking_ids = fields.One2many(
        'stock.picking', 'group_id', string='Pickings')
