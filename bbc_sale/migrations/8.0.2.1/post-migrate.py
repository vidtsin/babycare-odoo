# coding: utf-8
def migrate(cr, version):
    """ Reverse initial value of variant_published """
    if not version:
        return
    cr.execute(
        """ UPDATE product_product pp
        SET variant_published = true
        FROM product_template pt
        WHERE website_published is true
            AND pp.product_tmpl_id = pt.id """)
