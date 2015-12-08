# -*- coding; utf-8 -*-
from openerp import models, api
from openerp.tools.safe_eval import safe_eval


class Picking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def open_barcode_interface(self):
        """ Open barcode interface in new tab """
        res = super(Picking, self).open_barcode_interface()
        res['target'] = 'new'
        return res


class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    @api.multi
    def open_barcode_interface(self):
        """ Open barcode interface in new tab """
        res = super(PickingType, self).open_barcode_interface()
        res['target'] = 'new'
        return res
