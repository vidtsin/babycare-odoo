from openerp import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    remarks = fields.Char()
