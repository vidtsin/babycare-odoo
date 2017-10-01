Babycare Product Go-Live Checks
========================================

This module introduces some actions to check if a product template is ready to be published to Magento.

Three new actions in the more dropdown menu of the product template view:
==================================================
- Check Ready For Magento: loops through the selected records and checks if the required fields for synchronization to Magento are filled. In case fields are missing, a message will be displayed with the missing fields for each product.
- Update Internal References Config Products: loops through the selected records and updates the internal reference of variants of config products based on the attached bill of material. This action will only work if the calculated default_code has a length less or equal to 64. Otherwise, the default_code of the variant will stay empty.
- Update EAN13 and Images Config Products: loops through the selected records and updates the EAN13 and images of the variants of config products based on the attached bill of material. This action will only work if the product is a consumable and this consumable has only 1 line in attribute_line_ids. For all other products, EAN13 and Images must be filled manually.

Compatibility
=============
This module is compatible with OpenERP 8.0.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/babycarenl/babycare-odoo/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/babycarenl/babycare-odoo/issues/new?body=module:%20babycare_product_golive_checks%0Aversion:%208.0.0.1.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.