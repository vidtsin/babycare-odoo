# coding: utf-8
def migrate(cr, version):
    if not version:
        return
    cr.execute(
        """ DELETE FROM ir_translation
            WHERE module = 'babycare_product_brand'; """)
