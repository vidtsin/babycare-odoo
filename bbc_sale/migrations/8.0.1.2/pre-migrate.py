
# coding: utf-8
def migrate(cr, version):
    if not version:
        return
    for ref_res_id in (
            ('fispos_nl', 1),
            ('fispos_eu', 5),
            ('fispos_intra', 3),
            ('fispos_world', 4)):
        cr.execute(
            """ INSERT INTO ir_model_data (
            noupdate, name, module, model, res_id)
            SELECT true, %s, 'bbc_sale', 'account.fiscal.position', id
            FROM account_fiscal_position WHERE id = %s; """,
            ref_res_id)
