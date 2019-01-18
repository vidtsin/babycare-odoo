# coding: utf-8
from openerp import api, SUPERUSER_ID


def migrate(cr, version):
    """ Set templates inactive if the variants belong to the
    template are inactive as well. """
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    products = env['product.product'].search([
        '&',
        ('active', '=', False),
        ('variant_eol', '=', True),
        '|',
        ('bom_ids', '=', False),
        '&',
        ('bom_ids', '!=', False),
        ('prod_type', '=', 'simple')
    ])
    for product in products:
        template = product.mapped('product_tmpl_id')
        for temp in template:
            temp.write({'website_published': False})
            temp.write({'active': False})
