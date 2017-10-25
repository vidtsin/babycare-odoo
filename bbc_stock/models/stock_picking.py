# coding; utf-8
from openerp import api, fields, models
from openerp.addons.stock.stock import stock_picking as odoo_stock_picking


class Picking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'ir.needaction_mixin']

    @api.multi
    def open_barcode_interface(self):
        """ Open barcode interface in new tab """
        res = super(Picking, self).open_barcode_interface()
        res['target'] = 'new'
        return res

    @api.multi
    def _get_partner_address(self):
        for pick in self:
            if not pick.partner_id:
                pick.partner_address = ''
            else:
                pick.partner_address = pick.partner_id.with_context(
                    show_address=True).name_get()[0][1]

    partner_address = fields.Text(compute="_get_partner_address")

    @api.model
    def process_barcode_from_ui(self, picking_id, barcode_str, visible_op_ids):
        """ Add a couple of keys that will trigger sounds and behaviour in the
        interface """
        res = super(Picking, self.with_context(
            search_no_consu_single_attr=True)).process_barcode_from_ui(
                picking_id, barcode_str, visible_op_ids)
        if not res.get('filter_loc'):
            if res.get('operation_id'):
                if (picking_id and
                        self.browse(picking_id).location_dest_id
                        .usage == 'customer'):
                    ops = self.env['stock.pack.operation'].search(
                        [('picking_id', '=', picking_id)])
                    if not any(op.qty_done != op.product_qty
                               for op in ops):
                        res['done'] = True
                op = self.env['stock.pack.operation'].browse(
                    res['operation_id'])
                if op.qty_done > op.product_qty:
                    res['sound'] = 'error'
                else:
                    res['sound'] = 'success'
            else:
                res['sound'] = 'unknown'
        return res

    @api.model
    def action_done_from_ui(self, picking_id):
        """ Trigger a return to the menu by not passing on the next picking
        as per override of javascript done() method.
        """
        super(Picking, self).action_done_from_ui(picking_id)
        return False

    @api.model
    def _needaction_domain_get(self):
        """ Convert default search values in the context to needaction domain
        """
        domain = []
        if self.env.context.get('search_default_late'):
            domain.append(('max_date', '<', fields.Date.context_today(self)))
        if self.env.context.get('search_default_source_supplier'):
            domain.append(('location_id.usage', '=', 'supplier'))
        if self.env.context.get('search_default_dest_supplier'):
            domain.append(('location_dest_id.usage', '=', 'supplier'))
        if self.env.context.get('search_default_source_customer'):
            domain.append(('location_id.usage', '=', 'customer'))
        if self.env.context.get('search_default_dest_customer'):
            domain.append(('location_dest_id.usage', '=', 'customer'))
        if self.env.context.get('search_default_confirmed'):
            domain.append(
                ('state', 'in', ('confirmed', 'waiting', 'assigned')))
        if not domain:
            return [('id', '=', -1)]
        return domain

    def _register_hook(self, cr):
        """ Applying an inverse write method on an old API computed field.
        Reusing the same method that already exists for min_date, as it
        simply writes the date to all the picking's stock moves which will
        work for max_date just as well. """
        max_date = self._columns['max_date']
        max_date._fnct_inv = odoo_stock_picking._set_min_date
        max_date.readonly = False
        self._fields['max_date'].readonly = False
        return super(Picking, self)._register_hook(cr)


class PickingType(models.Model):
    _inherit = 'stock.picking.type'

    @api.multi
    def open_barcode_interface(self):
        """ Open barcode interface in new tab """
        res = super(PickingType, self).open_barcode_interface()
        res['target'] = 'new'
        return res
