# coding: utf-8
from openerp import api, SUPERUSER_ID


def migrate(cr, version):
    """ Set variants with x_availabilty less than 1 (e.g. 0
    or below 0) to variant_published = false. """
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['product.product'].search([
        ('x_availability', '<', 1),
        ('variant_eol', '=', True),
        ('variant_published', '=', True)
    ]).write({'variant_published': False})
