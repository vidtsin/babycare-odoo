# coding: utf-8
# Copyright (C) 2016 Opener B.V. <https://opener.am>
# @author Stefan Rijnhart <stefan@opener.am>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Babycare Sales customizations",
    "category": "Sale",
    "version": "8.0.2.3",
    "author": "Opener B.V.",
    "website": 'https://opener.am',
    "depends": [
        'website_sale',
        'sale_stock',
        'point_of_sale',
        'purchase',
        'mrp',
        'magento_bridge',  # Override of product view
    ],
    'data': [
        'data/account_fiscal_position.xml',
        'views/account_invoice.xml',
        'views/pos_order.xml',
        'views/templates.xml',
        'views/sale_order.xml',
        'views/product_public_category.xml',
        'views/purchase_order.xml',
        'views/stock_picking.xml',
        'views/stock_move.xml',
        'views/product.xml',
        'views/product_category.xml',
        'views/res_partner.xml',
        'data/ir_cron.xml',
        'data/action_automated_emails_magento.xml',
    ],
}
