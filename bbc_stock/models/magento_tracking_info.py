# coding: utf-8
from openerp import api, models


class TrackingInfo(models.Model):
    _inherit = 'magento.tracking.info'

    @api.multi
    def unlink(self):
        pickings = self.mapped('wk_picking_id')
        res = super(TrackingInfo, self).unlink()
        for picking in pickings:
            picking.number_of_packages = len(
                picking.magento_carrier_ids) or 1
        return res

    @api.model
    def create(self, vals):
        res = super(TrackingInfo, self).create(vals)
        if res.wk_picking_id:
            res.wk_picking_id.number_of_packages = len(
                res.wk_picking_id.magento_carrier_ids)
        return res
