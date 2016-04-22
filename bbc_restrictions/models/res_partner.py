# -*- coding: utf-8 -*-
##############################################################################
#
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from lxml import etree
from openerp import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        result = super(ResPartner, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar,
            submenu=submenu)
        if view_type != 'form':
            return result
        arch = etree.fromstring(result['arch'])
        for field in arch.xpath("//field[@name='state_id']"):
            field.attrib['options'] = \
                "{'no_create': true, 'no_open': true}"
        result['arch'] = etree.tostring(arch)
        return result
