# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012-2015 Therp BV (<http://therp.nl>).
#                          (C) 2016 Opener BV (<https://opener.am>).
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
{
    "name": "Baby care restrictions",
    "summary": "Prevent creation of records in various places",
    "category": "security",
    "version": "1.0",
    "author": "Therp BV,Opener BV",
    "depends": [
        'base',
        'sale',
        'point_of_sale',
    ],
    "data": [
        'views/sale_order.xml',
        'views/res_partner.xml',
        'views/pos_order.xml',
        'views/mrp_view.xml',
        'views/pricelist_view.xml',
    ],
}
