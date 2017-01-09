# coding: utf-8
from openerp import api, fields, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class PublicCategory(models.Model):
    _inherit = "product.public.category"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
    parent_id = fields.Many2one(ondelete='RESTRICT')

    @api.multi
    def unlink(self):
        if self.env['product.template'].search(
                [('public_categ_ids', 'in', self.ids)]):
            raise UserError(
                _('There are still products in these categories.'))
        return super(PublicCategory, self).unlink()
