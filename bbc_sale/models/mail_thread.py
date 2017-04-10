# coding: utf-8
from openerp import models, api
from openerp.addons.mail.mail_thread import mail_thread


@api.cr_uid_ids_context
def message_post(
        self, cr, uid, thread_id, body='', subject=None, type='notification',
        subtype=None, parent_id=False, attachments=None, context=None,
        content_subtype='html', **kwargs):
    if type == 'comment' and thread_id:
        if isinstance(thread_id, (int, long)):
            thread_id = [thread_id]
        order_ids = False
        if self._name == 'account.invoice':
            order_ids = self.pool['sale.order'].search(
                cr, uid, [('invoice_ids', '=', thread_id[0])])
        elif self._name == 'stock.picking':
            order_ids = self.pool['sale.order'].search(
                cr, uid, [
                    ('procurement_group_id.picking_ids', '=', thread_id[0]),
                ], context=context)
        if order_ids:
            context['default_model'] = 'sale.order'
            context['default_res_id'] = order_ids[0]
            return self.pool['sale.order'].browse(
                cr, uid, order_ids[0], context=context).message_post(
                    body=body, subject=subject, type=type,
                    subtype=subtype, parent_id=parent_id,
                    attachments=attachments,
                    content_subtype=content_subtype, **kwargs)
    return self.message_post_bbc_sale(
        cr, uid, thread_id,
        body=body, subject=subject, type=type,
        subtype=subtype, parent_id=parent_id,
        attachments=attachments, context=context,
        content_subtype=content_subtype, **kwargs)


class Thread(models.Model):
    _inherit = 'mail.thread'

    def _register_hook(self, cr):
        """ Monkeypatch """
        if not hasattr(mail_thread, 'message_post_bbc_sale'):
            mail_thread.message_post_bbc_sale = mail_thread.message_post
            mail_thread.message_post = message_post
        return super(Thread, self)._register_hook(cr)
