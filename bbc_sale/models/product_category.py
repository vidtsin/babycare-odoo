from openerp import models, api


class Category(models.Model):
    _inherit = 'product.category'
    _order = 'sequence asc, name'
