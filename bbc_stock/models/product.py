# coding: utf-8
from openerp import api, fields, models
from openerp.osv.expression import AND
from datetime import timedelta


class Product(models.Model):
    _inherit = 'product.product'

    max_incoming_stock_date = fields.Date(
        'Incoming stock expected at',
        compute='_compute_max_incoming_stock_date')
    max_incoming_stock_date_override = fields.Boolean(
        'Incoming stock date override')
    max_incoming_stock_date_override_value = fields.Date(
        'Incoming stock date value')

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.context.get('search_no_consu_single_attr'):
            args = AND([[('consu_single_attr', '=', False)], args])
        return super(Product, self).search(
            args, offset=offset, limit=limit, order=order, count=count)

    @api.onchange('max_incoming_stock_date_override')
    def onchange_max_incoming_stock_date_override(self):
        if not self.max_incoming_stock_date_override:
            self.max_incoming_stock_date_override_value = False

    @api.multi
    @api.depends('max_incoming_stock_date_override',
                 'max_incoming_stock_date_override_value',
                 'virtual_available')
    def _compute_max_incoming_stock_date(self):
        today = fields.Date.context_today(self)
        _dql, domain, _dmol = self._get_domain_locations()
        domain += [('state', 'not in', ('done', 'cancel', 'draft'))]

        def max_date_product(product):
            if product.max_incoming_stock_date_override:
                return product.max_incoming_stock_date_override_value
            dates_expected = self.env['stock.move'].search(
                domain + [('product_id', '=', product.id)],
                order='date_expected desc', limit=1).mapped(
                    'date_expected')
            base_date = dates_expected[0] if dates_expected else today
            delay = product.seller_ids[0].delay if product.seller_ids else 0
            return fields.Date.to_string(
                fields.Date.from_string(base_date) + timedelta(delay or 0))

        for product in self:
            if product.type == 'product':
                product.max_incoming_stock_date = max_date_product(product)
                continue
            bom = self.env['mrp.bom'].search(
                [('product_id', '=', product.id)],
                limit=1) or self.env['mrp.bom'].search(
                    [('product_tmpl_id', '=', product.product_tmpl_id.id)],
                    limit=1)
            if not bom:
                product.max_incoming_stock_date = False
                continue
            dates = []
            for line in bom.bom_line_ids:
                if (line.attribute_value_ids <= product.attribute_value_ids):
                    dates.append(max_date_product(line.product_id))
            product.max_incoming_stock_date = max(dates) if dates else today

    @api.model
    def update_product_availability(self):
        """ Reset expected stock date once we have incoming stock.
        TODO: refactor into an override of update_availability """
        res = super(Product, self).update_product_availability()
        self.search([
            ('x_availability', '>', 0),
            ('max_incoming_stock_date_override', '=', True),
        ]).write({
            'max_incoming_stock_date_override': False,
            'max_incoming_stock_date_override_value': False,
        })
        return res

    @api.model
    def reset_max_incoming_date_override(self):
        today = fields.Date.context_today(self)
        self.search([
            ('max_incoming_stock_date_override_value', '<=', today),
        ]).write({
            'max_incoming_stock_date_override': False,
            'max_incoming_stock_date_override_value': False,
        })
        return True
