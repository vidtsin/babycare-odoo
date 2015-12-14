import time
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api

logger = logging.getLogger('odoo.addons.bbc_sale')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    state = fields.Selection(
        selection_add=[('order', 'Can be ordered')])

    @api.multi
    def write(self, values):
        """
        Remove Buy route from products that are set to EOL
        """
        def add_route():
            route_ids = values.get('route_ids') or []
            route_ids.append(
                (4, self.env.ref('purchase.route_warehouse0_buy').id))
            values['route_ids'] = route_ids

        def del_route():
            route_ids = values.get('route_ids') or []
            route_ids.append(
                (3, self.env.ref('purchase.route_warehouse0_buy').id))
            values['route_ids'] = route_ids

        def inactive_orderpoints():
            self.env['stock.warehouse.orderpoint'].search(
                [('product_id.product_tmpl_id', 'in', self.ids)]).write(
                {'product_min_qty': 0.0, 'product_max_qty': 0.0})

        if values.get('state'):
            if values['state'] == 'end':
                del_route()
                inactive_orderpoints()
            elif values['state'] == 'obsolete':
                del_route()
                inactive_orderpoints()
            elif values['state'] == 'sellable':
                add_route()
            elif values['state'] == 'order':
                add_route()
                inactive_orderpoints()

        return super(ProductTemplate, self).write(values)

    @api.model
    def deactivate_obsolete_products(self):
        """ Products that have been set to EOL at least three months ago,
        have no physical stock and and that have no recent stock moves
        will be set to inactive. To be called from cron.
        """
        cutoff_datetime = fields.Date.to_string(
            datetime.now() - relativedelta(months=3))
        templates = self.search(
            [('state', 'in', ('end', 'obsolete')),
             ('write_date', '<', cutoff_datetime)])
        start_time = time.time()
        products = self.env['product.product'].search(
            [('product_tmpl_id', 'in', templates.ids),
             ('qty_available', '=', 0)])
        logger.debug(
            'Found %s candidate products in %s seconds to set inactive',
            len(products), time.time() - start_time)
        for product in products:
            if self.env['stock.move'].search(
                    [('product_id', '=', product.id),
                     ('write_date', '>', cutoff_datetime)]):
                logger.debug(
                    'Product %s has recent stock moves', product.id)
                continue
            logger.info(
                'Setting product %s to inactive', product.id)
            product.write({'active': False})
            if not self.env['product.product'].search(
                    [('product_tmpl_id', '=', product.product_tmpl_id.id)]):
                logger.debug(
                    'No active products for template %s. Setting inactive',
                    product.product_tmpl_id.id)
                product.product_tmpl_id.write({'active': False})

    def _register_hook(self, cr):
        """ Remove draft state """
        sel = self._columns['state'].selection
        self._columns['state'].selection = [
            (key, val) for key, val in sel if key != 'draft']
        self._fields['state'].selection = self._columns['state'].selection[:]
        return super(ProductTemplate, self)._register_hook(cr)

    @api.model
    def load(self, fields, data):
        """ Add context key to suppress creation of order points if missing """
        return super(
            ProductTemplate,
            self if self.env.context.get('no_autocreate_orderpoints')
            else self.with_context(no_autocreate_orderpoints=True)
        ).load(fields, data)


class Product(models.Model):
    _inherit = 'product.product'

    @api.model
    def update_product_availability(self):
        # Update the Website availability of the current product
        logger = logging.getLogger('odoo.addons.bbc_sale')
        offset = 0
        limit = 500
        start_time = time.time()
        product_exclude = []
        for bom in self.env['mrp.bom'].search([]):
            product_exclude += (
                bom.product_id and [bom.product_id.id] or
                bom.product_tmpl_id.product_variant_ids.ids)
        products = self.search(
            [('id', 'not in', product_exclude)],
            limit=limit, offset=offset)
        while products:
            for product in products:
                x_availability = (
                    product.virtual_available - product.incoming_qty)
                if product.x_availability != x_availability:
                    logger.debug(
                        "Updating availability of product %s from %s to %s",
                        product.default_code or product.name,
                        product.x_availability, x_availability)
                    product.write({'x_availability': x_availability})
            offset += limit
            products = self.search(
                [('id', 'not in', product_exclude)],
                limit=limit, offset=offset)

        for bom in self.env['mrp.bom'].search([]):
            # Update the Website availability of the parent templates' variants
            # Find all variants linked to this BoM
            for variant in (bom.product_id and [bom.product_id] or
                            bom.product_tmpl_id.product_variant_ids):
                avail = []
                for l in bom.bom_line_ids:
                    if set(l.attribute_value_ids).issubset(
                            set(variant.attribute_value_ids)):
                        avail.append(
                            int(l.product_id.x_availability / l.product_qty))
                x_availability = avail and min(avail) or 0
                if variant.x_availability != x_availability:
                    logger.debug(
                        "Updating availability of composed product %s from %s "
                        "to %s", variant.default_code or variant.name,
                        variant.x_availability, x_availability)
                    variant.write({'x_availability': x_availability})
        logger.debug(
            'Updated availability in %ss', time.time() - start_time)

    @api.model
    def load(self, fields, data):
        """ Add context key to suppress creation of order points if missing """
        return super(
            Product,
            self if self.env.context.get('no_autocreate_orderpoints')
            else self.with_context(no_autocreate_orderpoints=True),
        ).load(fields, data)

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        """ Create zero level orderpoints for each warehouse """
        res = super(Product, self).create(vals)
        if self.env.context.get('no_autocreate_orderpoints'):
            logger.debug('Suppressing autocreation of orderpoints')
        else:
            logger.debug('Autocreating of orderpoints')
            for warehouse in self.env['stock.warehouse'].search(
                    ['|', ('company_id', '=', self.env.user.company_id.id),
                     ('company_id', '=', False),
                     ('lot_stock_id', '!=', False)]):
                self.env['stock.warehouse.orderpoint'].create({
                    'warehouse_id': warehouse.id,
                    'location_id': warehouse.lot_stock_id.id,
                    'product_id': res.id,
                    'product_uom': res.uom_id.id,
                    'product_min_qty': 0.0,
                    'product_max_qty': 0.0,
                })
        return res
