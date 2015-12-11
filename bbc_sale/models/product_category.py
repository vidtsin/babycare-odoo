from openerp import models, api, fields


class Category(models.Model):
    _inherit = 'product.category'
    _order = 'parent_sequence, sequence'

    # Set a default for the existing sequence field
    sequence = fields.Integer(default=1)
    parent_sequence = fields.Integer(default=1, readonly=True)

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        print self._order
        return super(Category, self).search(args, offset=offset, limit=limit, order=order, count=count)

    @api.multi
    def write(self, vals):
        res = super(Category, self).write(vals)
        if self.ids:
            if 'parent_id' in vals:
                self.env.cr.execute(
                    """
                    UPDATE product_category pc
                    SET parent_sequence = parent.sequence
                    FROM product_category parent
                    WHERE pc.parent_id = parent.id
                    AND pc.id IN %s
                    """, (tuple(self.ids),))
            if 'sequence' in vals:
                self.env.cr.execute(
                    """
                    UPDATE product_category pc
                    SET parent_sequence = parent.sequence
                    FROM product_category parent
                    WHERE pc.parent_id = parent.id
                    AND parent.id IN %s
                    """, (tuple(self.ids),))
        return res
