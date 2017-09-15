# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    amount_free_shipping = fields.Float(
        'Free shipping from',
        help=('The amount from which purchase orders are shipped out free '
              'from this supplier'))
    pos_order_count = fields.Integer(
        compute='_pos_order_count', string='# of POS Orders')
    default_delay = fields.Integer(
        'Supplier delay',
        help='Default supplier delay when this supplier is linked to a product'
    )
    house_number = fields.Char('House number')
    house_number_addition = fields.Char('House number addition')

    @api.multi
    def _pos_order_count(self):
        for partner in self:
            partner.pos_order_count = len(
                self.env['pos.order'].search(
                    [('partner_id', '=', partner.id)]))

    @api.model
    def _commercial_fields(self):
        res = super(Partner, self)._commercial_fields()
        res.append('amount_free_shipping')
        return res

    @api.multi
    def name_get(self):
        res = []
        for partner in self:
            name = partner.name or ''
            if partner.parent_id and not \
                    partner.is_company and partner.parent_id.is_company:
                    name = "%s, %s" % (partner.parent_id.name, name)
            if self._context.get('show_address_only'):
                name = partner._display_address(without_company=True)
            if self._context.get('show_address'):
                name = name + "\n" + partner._display_address(
                    without_company=True)
                name = name.replace('\n\n', '\n')
                name = name.replace('\n\n', '\n')
            if self._context.get('show_email') and partner.email:
                name = "%s <%s>" % (name, partner.email)
            if self._context.get('html_format'):
                name = name.replace('\n', '<br/>')
            res.append((partner.id, name))
        return res

    @api.multi
    def _display_address(self, without_company=False):
        """
        Return an address formatted according to the country standards.

        :param address: browse record of the res.partner to format
        :returns: the address formatted in a display that fit its country
            habits (or the default ones if not country is specified)
        :rtype: string
        """
        # get the information that will be injected into the display format
        # get the address format
        if self.country_id.address_format:
            address_format = self.country_id.address_format.replace(
                '%(street)s',
                '%(street)s %(house_number)s %(house_number_addition)s')
            address_format = "%(wk_company)s\n" + address_format
        else:
            address_format = "%(wk_company)s\n%(street)s %(house_number)s \
                %(house_number_addition)s\n%(street2)s\n%(city)s \
                %(state_code)s %(zip)s\n%(country_name)s"
        args = {
            'wk_company': self.wk_company or '',
            'house_number': self.house_number or '',
            'house_number_addition': self.house_number_addition or '',
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self.country_id.name or '',
            'company_name': self.parent_id.is_company and
            self.parent_id.name or '',
        }
        for field in self._address_fields():
            args[field] = getattr(self, field) or ''
        if without_company:
            args['company_name'] = ''
        elif self.parent_id:
            address_format = '%(company_name)s\n' + address_format
        return address_format % args
