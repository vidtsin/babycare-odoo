# coding: utf-8
from openerp import api, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class PackOp(models.Model):
    _inherit = 'stock.pack.operation'

    @api.multi
    def write(self, vals):
        res = super(PackOp, self).write(vals)
        if 'qty_done' in vals and len(self):
            if (self.qty_done > self.product_qty
                    and self.location_dest_id.usage == 'customer'):
                raise UserError(
                    _('It is not allowed to deliver more items than have been '
                      'ordered. Please check the quantities on this picking.'))
        return res
