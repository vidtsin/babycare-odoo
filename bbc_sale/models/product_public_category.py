# coding: utf-8
from openerp import fields, models


class PublicCategory(models.Model):
    _inherit = "product.public.category"
    _parent_store = True
    _parent_order = 'sequence, name'
    _order = 'parent_left'

    parent_left = fields.Integer(index=True)
    parent_right = fields.Integer(index=True)
    parent_id = fields.Many2one(ondelete='RESTRICT')
