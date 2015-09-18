import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api


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

    @api.model
    def deactivate_obsolete_products(self):
        """ Products that have been set to EOL at least three months ago,
        and that have no recent stock moves will be set to inactive. To be
        called from cron.
        """
        logger = logging.getLogger('odoo.addons.bbc_sale')
        cutoff_datetime = fields.Date.to_string(
            datetime.now() - relativedelta(months=3))
        templates = self.search(
            [('state', 'in', ('end', 'obsolete')),
             ('write_date', '<', cutoff_datetime)])
        logger.debug(
            'Found %s candidate templates to set inactive', len(templates))
        for template in templates:
            logger.debug(
                'Template %s (%s) was modified at %s',
                template.id, template.state, template.write_date)
            products = self.env['product.product'].search(
                [('product_tmpl_id', '=', template.id)])
            if not products:
                logger.debug(
                    'No active products for this template. Setting inactive')
                template.write({'active': False})
                continue
            moves = self.env['stock.move'].search(
                [('product_id', 'in', products.ids),
                 ('write_date', '>', cutoff_datetime)])
            if moves:
                logger.debug(
                    'Recent stock moves: %s',
                    ','.join(['%s:%s' % (move.id, move.write_date)
                              for move in moves]))
                continue
            logger.info(
                'Setting products %s and template %s inactive',
                products.ids, template.id)
            products.write({'active': False})
            template.write({'active': False})
