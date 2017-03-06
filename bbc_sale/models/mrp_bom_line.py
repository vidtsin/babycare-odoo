# coding: utf-8
from openerp import api, models


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

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
