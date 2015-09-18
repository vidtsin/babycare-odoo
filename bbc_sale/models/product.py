from openerp import models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def write(self, values):
        """
        Remove Buy route from products that are set to EOL
        """
        if values.get('state') in ('end', 'obsolete'):
            route_ids = values.get('route_ids') or []
            route_ids.append(
                (3, self.env.ref('purchase.route_warehouse0_buy').id))
            values['route_ids'] = route_ids
        return super(ProductTemplate, self).write(values)
