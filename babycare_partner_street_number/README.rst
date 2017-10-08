Add an extra field house number addition
========================================

This extension introduces an extra field next to the street name and street number: street number addition.

Changes to the forked module partner_street_number
==================================================
- Introduce one new field for street number addition.
- Disabled _write_street function because street fields may not be overwritten due to courier export.
- Rewrites of _get_street and _address_fields functions to include the street number.
- Include _display_address function to disable the same function in Webkul code.
- Rearranged fields in the partner form and added some translations.

Compatibility
=============
This module is compatible with OpenERP 8.0.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/babycarenl/babycare-odoo/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/babycarenl/babycare-odoo/issues/new?body=module:%20babycare_partner_street_number%0Aversion:%208.0.0.1.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

This module is forked from the partner_street_number module of the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.