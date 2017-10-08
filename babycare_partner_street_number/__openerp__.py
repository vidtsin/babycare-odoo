{
    "name": "Babycare Extension: Street name and number",
    "summary": "Introduces new field for street number addition.",
    "version": "8.0.0.1.0",
    "author": "Wytze Jan Riedstra,Therp BV,Odoo Community Association (OCA)",
    "category": 'Tools',
    "depends": [
        'partner_street_number',
        'wk_base_partner_patch',
    ],
    "data": [
        'views/res_partner.xml',
    ],
    'license': 'AGPL-3',
}
