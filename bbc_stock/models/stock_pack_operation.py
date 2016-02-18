# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Opener B.V. (<https://opener.am>).
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
from openerp import models, fields, api


class Operation(models.Model):
    _inherit = 'stock.pack.operation'

    @api.multi
    @api.depends('product_qty', 'qty_done')
    def _get_sequence(self):
        for operation in self:
            if not operation.product_qty:
                # Not on the original picking
                operation.sequence = 0
            elif not operation.qty_done:
                # Still to scan
                operation.sequence = 30
            elif operation.qty_done > operation.product_qty:
                # Excess amount
                operation.sequence = 10
            elif operation.qty_done == operation.product_qty:
                # Satisfied
                operation.sequence = 999
            else:
                # partially scanned
                operation.sequence = 20
            print operation.product_id.name, operation.sequence

    _order = 'sequence, write_date desc'
    sequence = fields.Integer(compute="_get_sequence", store=True)
