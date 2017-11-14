# coding: utf-8
from openerp import api, SUPERUSER_ID


def migrate(cr, version):
    """ Set server actions for the workflow activities sale_router
    and account_paid """
    if not version:
        return
    env = api.Environment(cr, SUPERUSER_ID, {})
    action_sale_confirmation_xmlid = env.ref(
        'bbc_sale.action_send_email_confirmation_sales_order_magento').id
    action_invoice_validation_xmlid = env.ref(
        'bbc_sale.action_send_email_validation_invoice_magento').id
    wkf_sale_xmlid = env.ref('sale.wkf_sale').id
    wkf_invoice_xmlid = env.ref('account.wkf').id
    wkf_activity_sale = env['workflow.activity'].search(
        [('name', '=', 'router'), ('wkf_id', '=', wkf_sale_xmlid)])
    wkf_activity_invoice = env['workflow.activity'].search(
        [('name', '=', 'paid'), ('wkf_id', '=', wkf_invoice_xmlid)])
    wkf_activity_sale.write({'action_id': action_sale_confirmation_xmlid})
    wkf_activity_invoice.write({'action_id': action_invoice_validation_xmlid})
