# -*- coding: utf-8 -*-
from openerp import models, fields


class Category(models.Model):
    _inherit = 'product.category'

    # Set a default for the existing sequence field
    sequence = fields.Integer(default=1)
