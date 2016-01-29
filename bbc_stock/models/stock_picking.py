# -*- coding; utf-8 -*-
from openerp import api, fields, models


class Picking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def open_barcode_interface(self):
        """ Open barcode interface in new tab """
        res = super(Picking, self).open_barcode_interface()
        res['target'] = 'new'
        return res

    @api.multi
    def _get_partner_address(self):
        for pick in self:
            if not pick.partner_id:
                pick.partner_address = ''
            else:
                pick.partner_address = pick.partner_id.with_context(
                    show_address=True).name_get()[0][1]

    partner_address = fields.Text(compute="_get_partner_address")


class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    @api.multi
    def open_barcode_interface(self):
        """ Open barcode interface in new tab """
        res = super(PickingType, self).open_barcode_interface()
        res['target'] = 'new'
        return res
