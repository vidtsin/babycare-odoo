# -*- coding: utf-8 -*-
from openerp import models, api
from openerp.exceptions import Warning as UserError


class ProductAttributeManager(models.Model):
    _name = 'product.attributemanager'

    """
    all brands have their own sync action because brands are within their own
    model product.brand and not within our model custom.option
    """
    @api.multi
    def action_call_magento_sync_all_brands(self):
        self.env['magento.synchronization'].syncAllBrands()

    @api.multi
    def action_call_magento_sync(self):
        option_type = self.env.context.get('option_type')
        if not option_type:
            raise UserError(
                'action_call_magento_sync_all was called without an option '
                'type.')
        self.env['magento.synchronization'].syncCustomOption(option_type)
