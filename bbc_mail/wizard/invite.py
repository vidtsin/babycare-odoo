# coding: utf-8
from openerp import models, fields


class InviteWizard(models.TransientModel):
    _inherit = 'mail.wizard.invite'

    send_mail = fields.Boolean(default=False)
