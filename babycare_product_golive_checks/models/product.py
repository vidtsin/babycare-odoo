# -*- coding: utf-8 -*-
from openerp import models, api
from openerp.tools.translate import _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def check_ready_for_magento(self):
        text = ''
        not_image_ids = []
        not_magento_type_ids = []
        not_short_description_ids = []
        not_long_description_ids = []
        not_ean13_ids = []
        not_reference_ids = []
        not_weight_ids = []
        not_pubcategorie_ids = []
        not_published_ids = []
        not_magento_attset_ids = []
        not_wk_website_ids = []
        not_variant_reference_ids = []
        not_variant_ean13_ids = []
        success_ids = []
        for template_id in self._context.get('active_ids'):
            template = self.env['product.template'].browse(template_id)
            if not template.image_medium:
                not_image_ids.append(template.name)
            if not template.prod_type:
                not_magento_type_ids.append(template.name)
            if not template.description_sale:
                not_short_description_ids.append(template.name)
            if not template.description:
                not_long_description_ids.append(template.name)
            if not template.ean13 and template.type == 'product':
                not_ean13_ids.append(template.name)
            if not template.default_code:
                not_reference_ids.append(template.name)
            if not template.weight_net:
                not_weight_ids.append(template.name)
            if not template.public_categ_ids:
                not_pubcategorie_ids.append(template.name)
            if not template.website_published:
                not_published_ids.append(template.name)
            if not template.attribute_set_id:
                not_magento_attset_ids.append(template.name)
            if not template.wk_websites_id:
                not_wk_website_ids.append(template.name)
            if template.type == 'consu':
                variant_ids = template.product_variant_ids.ids
                variant_reference = self.env['product.product'].search(
                    [('id', 'in', variant_ids), ('default_code', '=', False)])
                variant_ean13 = self.env['product.product'].search(
                    [('id', 'in', variant_ids), ('ean13', '=', False)])
                if variant_reference:
                    not_variant_reference_ids.append(template.name)
                if variant_ean13:
                    not_variant_ean13_ids.append(template.name)
                if template.image_medium and template.prod_type and \
                    template.description_sale and template.description and \
                    template.weight_net and template.public_categ_ids and \
                    template.website_published and template.attribute_set_id \
                    and template.wk_websites_id and not variant_reference \
                        and not variant_ean13:
                    success_ids.append(template.name)
            if template.type == 'product':
                if template.image_medium and template.prod_type and \
                    template.description_sale and template.description and \
                    template.ean13 and template.default_code and \
                    template.weight_net and template.public_categ_ids and \
                    template.website_published and template.attribute_set_id \
                        and template.wk_websites_id:
                    success_ids.append(template.name)
        if not_image_ids:
            text += _("\n\nImage is missing:\n%s") % (
                '\n'.join(not_image_ids))
        if not_magento_type_ids:
            text += _("\n\nMagento type is missing:\n%s") % (
                '\n'.join(not_magento_type_ids))
        if not_short_description_ids:
            text += _("\n\nShort description is missing:\n%s") % (
                '\n'.join(not_short_description_ids))
        if not_long_description_ids:
            text += _("\n\nLong description is missing:\n%s") % (
                '\n'.join(not_long_description_ids))
        if not_ean13_ids:
            text += _("\n\nEAN13 is missing:\n%s") % (
                '\n'.join(not_ean13_ids))
        if not_reference_ids:
            text += _("\n\nInternal reference is missing:\n%s") % (
                '\n'.join(not_reference_ids))
        if not_weight_ids:
            text += _("\n\nNet weight is missing:\n%s") % (
                '\n'.join(not_weight_ids))
        if not_pubcategorie_ids:
            text += _("\n\nPublic category is missing:\n%s") % (
                '\n'.join(not_pubcategorie_ids))
        if not_published_ids:
            text += _("\n\nNot published:\n%s") % (
                '\n'.join(not_published_ids))
        if not_magento_attset_ids:
            text += _("\n\nMagento attribute set in missing:\n%s") % (
                '\n'.join(not_magento_attset_ids))
        if not_wk_website_ids:
            text += _("\n\nMagento website is missing:\n%s") % (
                '\n'.join(not_wk_website_ids))
        if not_variant_reference_ids:
            text += _("\n\nInternal reference is missing for one or more"
                      " variants of:\n%s") % (
                          '\n'.join(not_variant_reference_ids))
        if not_variant_ean13_ids:
            text += _("\n\nEAN13 is missing for one or more variants"
                      " of:\n%s") % (
                          '\n'.join(not_variant_ean13_ids))
        if success_ids:
            text += _("\n\nReady:\n%s") % ('\n'.join(success_ids))
        partial = self.env['message.wizard'].create({'text': text})
        return {
            'name': _("Message"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'message.wizard',
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
        }

    @api.model
    def update_internal_references_config_product(self):
        text = ''
        succes_ids = []
        error_len_ids = []
        error_ids = []
        for template_id in self._context.get('active_ids'):
            template = self.env['product.template'].browse(template_id)
            reference = template.bom_ids.product_id.default_code
            if template.type == 'consu':
                for b in template.bom_ids:
                    for variant in (b.product_id and
                                    [b.product_id] or
                                    b.product_tmpl_id.product_variant_ids):
                        reference = []
                        for l in b.bom_line_ids:
                            if set([al.id for al in l.attribute_value_ids]).\
                                    issubset(set([vl.id for vl
                                             in variant.attribute_value_ids])):
                                if l.product_qty == 1:
                                    prodqty = ""
                                else:
                                    prodqty0 = int(l.product_qty)
                                    prodqty = str(prodqty0) + "x "
                                prodref = l.product_id.default_code
                                prodappend = prodqty + prodref
                                reference.append(prodappend)
                        reference = ' + '.join([str(el) for el in reference])
                        if len(reference) > 64:
                            error_len_ids.append(template.name)
                        else:
                            variant.write({'default_code': reference})
                succes_ids.append(template.name)
            else:
                error_ids.append(template.name)
        if succes_ids:
            text += _("\n\nFollowing config product(s) is/are updated with"
                      " internal references:\n%s") % ('\n'.join(succes_ids))
        if error_len_ids:
            text += _("\n\nFollowing config product(s) is/are not (completely)"
                      " updated because (some) references are"
                      " too long:\n%s") % ('\n'.join(error_len_ids))
        if error_ids:
            text += _("\n\nFollowing product(s) is/are not updated because"
                      " they are not config products:\n%s") % (
                          '\n'.join(error_ids))
        partial = self.env['message.wizard'].create({'text': text})
        return {
            'name': _("Message"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'message.wizard',
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
        }

    @api.model
    def update_ean13_images_config_product(self):
        text = ''
        succes_ids = []
        error_ids = []
        for template_id in self._context.get('active_ids'):
            template = self.env['product.template'].browse(template_id)
            if template.configurable:
                for b in template.bom_ids:
                    for variant in (b.product_id and
                                    [b.product_id] or
                                    b.product_tmpl_id.product_variant_ids):
                        for l in b.bom_line_ids:
                            if set([al.id for al in l.attribute_value_ids]).\
                                    issubset(set([vl.id for vl
                                             in variant.attribute_value_ids])):
                                    prod_ean13 = l.product_id.ean13
                                    prod_image = l.product_id.image
                        variant.write({'ean13': prod_ean13})
                        variant.write({'image': prod_image})
                succes_ids.append(template.name)
            else:
                error_ids.append(template.name)
        if succes_ids:
            text += _("\n\nFollowing config product(s) is/are updated with"
                      " EAN13 and images:\n%s") % ('\n'.join(succes_ids))
        if error_ids:
            text += _("\n\nFollowing config product(s) is/are not updated"
                      " because it is not a config product or a config"
                      " product with more than two attributes:\n%s") % (
                          '\n'.join(error_ids))
        partial = self.env['message.wizard'].create({'text': text})
        return {
            'name': _("Message"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'message.wizard',
            'res_id': partial.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
        }
