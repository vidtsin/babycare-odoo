# -*- coding: utf-8 -*-
from openerp import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.one
    @api.depends('street_name', 'street_number', 'street_number_addition')
    def _get_street(self):
        self.street = ' '.join(
            filter(None, [self.street_name, self.street_number,
                          self.street_number_addition]))

    @api.model
    def _display_address(self, address, without_company=False):
        """
        Inject a context key to prevent the 'street' name to be
        deleted from the result of _address_fields when called from
        the super.
        """
        return super(Partner, self.with_context(display_address=True)).\
            _display_address(address, without_company=without_company)

    @api.model
    def _address_fields(self):
        """
        Pass on the fields for address synchronisation to contacts.

        This method is used on at least two occassions:
        [1] when address fields are synced to contacts, and
        [2] when addresses are formatted
        We want to prevent the 'street' field to be passed in the
        first case, as it has a fallback write method which should
        not be triggered in this case, while leaving the field in
        in the second case. Therefore, we remove the field
        name from the list of address fields unless we find the context
        key that this module injects when formatting an address.
        Could have checked for the occurrence of the synchronisation
        method instead, leaving the field in by default but that could
        lead to silent data corruption should the synchronisation API
        ever change.
        """
        res = super(Partner, self)._address_fields()
        if 'street' in res and not (
                self._context.get('display_address')):
            res.remove('street')
        return res + ['street_number_addition']

    street_number_addition = fields.Char('Street number addition')
    street_number = fields.Char(size=5)
