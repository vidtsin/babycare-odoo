# coding: utf-8
from openerp import models, fields, api


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    product_id = fields.Many2one(
        domain=[('sale_ok', '=', True), ('consu_single_attr', '=', False)])

    @api.model
    def create(self, vals):
        res = super(MrpBomLine, self).create(vals)
        self.bom_id.update_availability()
        return res

    @api.multi
    def write(self, vals):
        res = super(MrpBomLine, self).write(vals)
        self.mapped('bom_id').update_availability()
        return res
