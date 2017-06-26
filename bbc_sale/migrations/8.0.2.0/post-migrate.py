# coding: utf-8
from openerp import api, SUPERUSER_ID


def migrate(cr, version):
    """ Set variants of eol products to eol. This will trigger setting
    bom variants to eol if one of their components is.
    Set variant_published according to the value of website_published
    of their templates. """
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    env['product.template'].search(
        [('state', 'in', ('end', 'obsolete'))]
    ).mapped('product_variant_ids').write({'variant_eol': True})

    env.cr.execute(
        """ UPDATE product_product pp
        SET variant_published = false
        FROM product_template pt
        WHERE website_published = false
            AND pp.product_tmpl_id = pt.id """)
