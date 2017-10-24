# coding: utf-8
import logging
from openerp import api, SUPERUSER_ID


def migrate(cr, version):
    """ Reset value of 'configurable' on templates according to the new
    definition """
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    templates = env['product.attribute.line'].search([
        ('product_tmpl_id.configurable', '=', False),
        ('product_tmpl_id.type', '=', 'consu'),
    ]).mapped('product_tmpl_id').filtered('attribute_line_ids')
    logging.getLogger(__name__).info(
        'Recomputing the value for \'configurable\' of %s '
        'templates' % len(templates))
    templates.write({'type': 'consu'})
