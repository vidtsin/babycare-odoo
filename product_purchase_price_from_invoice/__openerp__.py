# coding: utf-8
# Copyright (C) 2014 Therp BV <http://therp.nl>.
#           (C) 2017 Opener B.V. <https://opener.am>
# @author Stefan Rijnhart <stefan@opener.am>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# coding: utf-8
{
    "name": "Update supplier product prices from the invoice view",
    "version": "8.0.1.0.0",
    "author": "Therp BV",
    "license": "AGPL-3",
    "description": """
Allows to manage per-supplier prices directly from the invoice
""",
    "category": "Accounting & Finance",
    "depends": [
        'product_standard_margin',
        'account',
    ],
    "data": [
        'views/account_invoice_updateprice.xml',
    ],
}
