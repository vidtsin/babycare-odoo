# -*- coding: utf-8 -*-
from openerp import models, fields


class Category(models.Model):
    _inherit = 'product.category'
    _order = 'parent_sequence, sequence'

    # Set a default for the existing sequence field
    sequence = fields.Integer(default=1)
