# coding: utf-8
import time
import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api
from openerp.exceptions import ValidationError
from openerp.tools.translate import _

logger = logging.getLogger('odoo.addons.bbc_sale')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    state = fields.Selection(
        selection_add=[('order', 'Can be ordered')])
    supplier_code = fields.Char(
        related='seller_ids.product_code', readonly=True)
    description = fields.Text('Long description')
    description_sale = fields.Text('Short description')
    display_code = fields.Char(compute='get_configurable')
    is_component = fields.Boolean(
        compute='compute_is_component',
        search='search_is_component')
    bom_component_count = fields.Integer(
        compute="compute_bom_component_count")
    x_availability = fields.Float('Website availability', default=0)
    configurable = fields.Boolean(
        compute='get_configurable', store=True)
    is_synced_magento = fields.Boolean(
        'Synced to Magento',
        compute='compute_is_synced_magento',
        search='search_is_synced_magento')

    @api.multi
    @api.depends('type', 'bom_ids', 'attribute_line_ids')
    def get_configurable(self):
        """ Compute if a product is configurable, and if it is, mask the
        default code with a label 'configurable' """
        for template in self:
            if (template.type == 'consu' and template.bom_ids and
                    template.attribute_line_ids):
                template.configurable = True
                template.display_code = 'Configurabel'
            else:
                template.configurable = False
                template.display_code = template.default_code

    @api.multi
    def compute_bom_component_count(self):
        for template in self:
            template.bom_component_count = len(
                self.env['mrp.bom.line'].search(
                    [('product_id', 'in', template.product_variant_ids.ids)]
                ).mapped('bom_id'))

    @api.multi
    def compute_is_component(self):
        for template in self:
            template.is_component = bool(
                self.env['mrp.bom.line'].search([
                    ('product_id', 'in', template.product_variant_ids.ids)
                ], limit=1))

    @api.model
    def search_is_component(self, operator, value):
        negate = not bool(value)
        if operator in ('!=', '<>'):
            negate = not negate
        templates = self.env['mrp.bom.line'].search(
            []).mapped('product_id.product_tmpl_id')
        return [('id', 'not in' if negate else 'in', templates.ids)]

    @api.multi
    def compute_is_synced_magento(self):
        synced = self.env['magento.product.template'].search(
            [('erp_template_id', 'in', self.ids)]).mapped('erp_template_id')
        for template in self:
            template.is_synced_magento = template.id in synced

    @api.model
    def search_is_synced_magento(self, operator, value):
        negate = not bool(value)
        if operator in ('!=', '<>'):
            negate = not negate
        templates = self.env['magento.product.template'].search([
            ('erp_template_id', 'not in', (False, 0))]).mapped(
            'erp_template_id')
        return [('id', 'not in' if negate else 'in', templates)]

    @api.multi
    def write(self, values):
        """
        Remove Buy route from products that are set to EOL.
        Propagate state and website_published to the underlying variants
        for nonconfigurable templates.
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

        nonconfigurable = self.filtered(lambda t: not t.configurable)
        if values.get('state') in ('end', 'obsolete'):
            del_route()
            inactive_orderpoints()
            if self.env.context.get('propagate_state', True):
                to_eol = nonconfigurable.mapped(
                    'product_variant_ids').filtered(
                        lambda p: not p.variant_eol)
                if to_eol:
                    to_eol.write({'variant_eol': True})
        elif values.get('state'):
            if values['state'] == 'sellable':
                add_route()
            if values['state'] == 'draft':
                add_route()
                inactive_orderpoints()
            if self.env.context.get('propagate_state', True):
                un_eol = nonconfigurable.mapped(
                    'product_variant_ids').filtered(
                        lambda p: p.variant_eol)
                if un_eol:
                    un_eol.write({'variant_eol': False})

        if 'website_published' in values and self.env.context.get(
                'propagate_state', True):
            if values['website_published']:
                publish = self.mapped(
                    'product_variant_ids').filtered(
                        lambda p: not p.variant_published and
                        not p.variant_eol)
            else:
                publish = nonconfigurable.mapped(
                    'product_variant_ids').filtered(
                        lambda p: p.variant_published)
            if publish:
                publish.write(
                    {'variant_published': values['website_published']})

        return super(ProductTemplate, self).write(values)

    @api.model
    def deactivate_obsolete_products(self):
        """ Products that have been set to EOL at least three months ago,
        have no physical stock and and that have no recent stock moves
        will be set to inactive. To be called from cron.

        Legacy note: works on product products even if defined on
        product.template.
        """
        cutoff_datetime = fields.Date.to_string(
            datetime.now() - relativedelta(months=3))
        start_time = time.time()
        products = self.env['product.product'].search([
            ('variant_eol', '=', True),
            ('write_date', '<', cutoff_datetime),
            ('qty_available', '=', 0),
            ('bom_ids', '=', False)])
        logger.debug(
            'Found %s candidate products in %s seconds to set inactive',
            len(products), time.time() - start_time)
        for product in products:
            if self.env['stock.move'].search([
                    ('product_id', '=', product.id),
                    ('write_date', '>', cutoff_datetime)]):
                logger.debug(
                    'Product %s has recent stock moves', product.id)
                continue
            logger.info(
                'Setting product %s to inactive', product.id)
            product.write({'active': False})

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
        self = (
            self if self.env.context.get('no_autocreate_orderpoints')
            else self.with_context(no_autocreate_orderpoints=True))
        self = (
            self if self.env.context.get('set_seller_default_delay')
            else self.with_context(set_seller_default_delay=True))
        return super(ProductTemplate, self).load(fields, data)


class Product(models.Model):
    _inherit = 'product.product'

    is_component = fields.Boolean(
        compute='compute_is_component',
        search='search_is_component')
    consu_single_attr = fields.Boolean(
        compute='get_consu_single_attr',
        string='Consumable with just one attribute',
        store=True)
    variant_eol = fields.Boolean(
        'Variant is end-of-life', readonly=True)
    variant_published = fields.Boolean(
        'Variant is published', readonly=True)
    blue = fields.Boolean(
        compute='_compute_blue',
        string='Show as blue in tree view')
    is_synced_magento = fields.Boolean(
        'Synced to Magento',
        compute='compute_is_synced_magento',
        search='search_is_synced_magento')
    # Prevent copying fields that are forced to be unique
    default_code = fields.Char(copy=False)
    ean13 = fields.Char(copy=False)

    @api.multi
    def _constraint_unique_codes(self):
        """ Check that product code and ean13 is unique except for
        configurable products """
        for product in self:
            if product.configurable:
                continue
            for field in ['default_code', 'ean13']:
                if not product[field]:
                    continue
                if self.search([
                        ('id', '!=', self.id),
                        (field, '=', product[field]),
                        ('configurable', '=', False)]):
                    raise ValidationError(_(
                        'A product with value "%s" for field "%s" already '
                        'exists.') % (product[field], field))
        return True

    _constraints = [(
        _constraint_unique_codes,
        'A product with this code already exists',
        ['ean13', 'default_code'],
    )]

    @api.multi
    @api.depends('product_tmpl_id.configurable', 'variant_eol',
                 'state', 'virtual_available')
    def _compute_blue(self):
        for product in self:
            if product.configurable:
                product.blue = product.variant_eol
            else:
                product.blue = (
                    product.virtual_available >= 0 and product.state in (
                        'draft', 'end', 'obsolete'))

    @api.multi
    @api.depends('type', 'attribute_value_ids')
    def get_consu_single_attr(self):
        for product in self:
            if product.type == 'consu' and len(
                    product.attribute_value_ids) == 1:
                product.consu_single_attr = True
            else:
                product.consu_single_attr = False

    @api.multi
    def compute_is_component(self):
        for product in self:
            product.is_component = bool(
                self.env['mrp.bom.line'].search([
                    ('product_id', '=', product.id)
                ], limit=1))

    @api.model
    def search_is_component(self, operator, value):
        negate = not bool(value)
        if operator in ('!=', '<>'):
            negate = not negate
        products = self.env['mrp.bom.line'].search(
            []).mapped('product_id')
        return [('id', 'not in' if negate else 'in', products.ids)]

    @api.multi
    def compute_is_synced_magento(self):
        synced = self.env['magento.product'].search([
            ('oe_product_id', '=', self.ids)]).mapped('oe_product_id')
        for product in self:
            product.is_synced_magento = product.id in synced

    @api.model
    def search_is_synced_magento(self, operator, value):
        negate = not bool(value)
        if operator in ('!=', '<>'):
            negate = not negate
        products = self.env['magento.product'].search([
            ('oe_product_id', 'not in', (False, 0))]).mapped('oe_product_id')
        return [('id', 'not in' if negate else 'in', products)]

    @api.multi
    def update_availability(self):
        """ Update the Website availability of the current product. Unpublish
        end-of-life stockable/consumable products that are not available
        anymore.
        """
        bom_lines = self.env['mrp.bom'].search([
            '|', ('product_id', 'in', self.ids),
            ('product_tmpl_id', '=', self.mapped('product_tmpl_id').ids)])
        exclude_products = bom_lines.mapped('product_id') + bom_lines.mapped(
            'product_tmpl_id.product_variant_ids')
        for product in self:
            if product in exclude_products:
                continue
            x_availability = product.virtual_available - product.incoming_qty
            if (product.x_availability != x_availability or
                    product.x_availability is False):
                product.write({'x_availability': x_availability})
            mage_product_mapping = self.env['magento.product'].search([
                ('oe_product_id', 'in', self.ids)])
            mage_product_mapping.write({'stock_need_sync': True})

        boms = self.env['mrp.bom'].search([
            ('bom_line_ids.product_id', 'in', self.ids),
        ])
        affected = self + boms.update_availability()

        to_unpublish = self.env['product.product'].search([
            ('id', 'in', affected.ids),
            ('x_availability', '=', 0),
            ('variant_eol', '=', True),
            ('variant_published', '=', True),
        ])
        if to_unpublish:
            to_unpublish.write({'variant_published': False})

    @api.model
    def update_product_availability(self):
        """ Wrapper around update_availability. Call from cron.

        This is a nightly sweep up which should be (mostly?) redundant as
        update_availability is already called from the relevant operations
        on stock moves and inventories. """
        logger = logging.getLogger('odoo.addons.bbc_sale')
        offset = 0
        limit = 500
        start_time = time.time()
        domain = [('type', 'in', ('product', 'consu'))]
        products = self.search(domain, limit=limit, offset=offset)
        while products:
            products.update_availability()
            offset += limit
            products = self.search(domain, limit=limit, offset=offset)

        logger.debug(
            'Updated availability in %ss', time.time() - start_time)

    @api.model
    def load(self, fields, data):
        """ Add context key to suppress creation of order points if missing """
        self = (
            self if self.env.context.get('no_autocreate_orderpoints')
            else self.with_context(no_autocreate_orderpoints=True))
        self = (
            self if self.env.context.get('set_seller_default_delay')
            else self.with_context(set_seller_default_delay=True))
        return super(Product, self).load(fields, data)

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
        if 'variant_published' not in vals and (
                res.product_tmpl_id.website_published):
            res.write({'variant_published': True})
        return res

    @api.multi
    def compute_bom_component_count(self):
        for product in self:
            product.bom_component_count = len(
                self.env['mrp.bom.line'].search(
                    [('product_id', '=', product.id)]).mapped('bom_id'))

    bom_component_count = fields.Integer(
        compute="compute_bom_component_count")

    @api.multi
    def write(self, vals):
        """ For non configurable products, propagate variant_published and
        variant_eol to the template"""
        res = super(Product, self).write(vals)
        nonconfigurable = self.mapped('product_tmpl_id').filtered(
            lambda t: not t.configurable)
        if 'variant_eol' in vals:
            self.set_bom_line_variant_eol()
            if vals['variant_eol']:
                for template in nonconfigurable:
                    if template.state in ('end', 'obsolete'):
                        continue
                    if all(variant.variant_eol
                           for variant in template.product_variant_ids):
                        template.with_context(propagate_state=False).write(
                            {'state': 'end'})
            else:
                if 'variant_published' not in vals:
                    # If template is published, now that variant_eol has been
                    # set to false we can republish this variant.
                    to_publish = self.filtered(
                        lambda p: p.product_tmpl_id.configurable and
                        p.product_tmpl_id.website_published)
                    if to_publish:
                        super(Product, to_publish).write({
                            'variant_published': True})
                for template in self.mapped('product_tmpl_id'):
                    if template.state not in ('draft', 'sellable'):
                        template.with_context(propagate_state=False).write(
                            {'state': 'sellable'})
        if 'variant_published' in vals:
            if not vals['variant_published']:
                for template in self.mapped('product_tmpl_id'):
                    if template.website_published and all(
                            not variant.variant_published
                            for variant in template.product_variant_ids):
                        template.with_context(propagate_state=False).write(
                            {'website_published': False})
            else:
                for template in nonconfigurable:
                    if not template.website_published:
                        template.with_context(propagate_state=False).write(
                            {'website_published': True})
        return res

    @api.multi
    def set_bom_line_variant_eol(self):
        """ If a component is end-of-life, set variants with the component
        in its BOM to variant_eol """
        bom_lines = self.env['mrp.bom.line'].search([
            ('product_id', 'in', self.ids)])
        eol_variants = self.env['product.product']
        for bom_line in bom_lines:
            if bom_line.bom_id.product_id:
                variants = bom_line.bom_id.product_id
            else:
                variants = bom_line.bom_id.product_tmpl_id.product_variant_ids
            for variant in variants.filtered(
                    lambda v: v.variant_eol != self[0].variant_eol):
                if bom_line.attribute_value_ids <= variant.attribute_value_ids:
                    eol_variants += variant
        if eol_variants:
            eol_variants.write({'variant_eol': self[0].variant_eol})
