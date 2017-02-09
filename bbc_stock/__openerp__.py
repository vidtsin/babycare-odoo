# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Opener B.V. (<https://opener.am>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU LGPL as
#    published by the Free Software Foundation, either version 2 of the
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
    "name": "Babycare Stock customizations",
    "category": "Stock",
    "version": "1.0",
    "author": "Opener B.V.",
    "website": 'https://opener.am',
    "depends": [
        # NB keep the dependency on stock even though delivery already depends
        # on stock, because it seems like the webclient does not do transitive
        # dependencies...
        'stock',
        'delivery',
        'bbc_sale',
        'mob_tracking',
    ],
    'data': [
        'views/assets.xml',
        'views/product.xml',
        'data/ir_cron.xml',
    ],
    'qweb': ['static/src/xml/picking.xml'],
}
