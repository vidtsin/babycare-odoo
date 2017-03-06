# coding: utf-8
import logging

from openerp import api, models


_logger = logging.getLogger(__name__)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.multi
    def update_availability(self):
        for bom in self:
            for variant in (bom.product_id or
                            bom.product_tmpl_id.product_variant_ids):
                avail = []
                for line in bom.bom_line_ids:
                    if (line.attribute_value_ids <=
                            variant.attribute_value_ids):
                        avail.append(
                            int(line.product_id.x_availability /
                                line.product_qty))
                x_availability = avail and min(avail) or 0
                if variant.x_availability != x_availability:
                    _logger.debug(
                        "Updating availability of composed product %s "
                        "from %s to %s",
                        variant.default_code or variant.name,
                        variant.x_availability, x_availability)
                    variant.x_availability = x_availability

    @api.model
    def create(self, vals):
        res = super(MrpBom, self).create(vals)
        self.update_availability()
        return res

    @api.multi
    def write(self, vals):
        res = super(MrpBom, self).write(vals)
        self.update_availability()
        return res
