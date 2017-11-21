Product Attribute Manager [babycare_product_brand]
=====================================

This module allows Odoo users to easily manage product attributes.
Currently, the following attributes are supported:

 * Product Brand
 * Product Color
 * Warranty
 * Buggies Adjustable Backrest (selection-field)
 * Buggies Age Category
 * Buggies Maximum Carry Weight
 * Buggies Number of Wheels
 * Carriers Direction of Use
 * Carriers Maximum Carry Weight
 * Carriers Type
 * Car Seats Age Category
 * Car Seats Child Length
 * Car Seats Child Weight
 * Car Seats Direction of Use
 * Car Seats Install Method
 * Clothes Gender (selection-field)
 * Clothes Season
 * Clothes Size
 * High Chairs Age Category
 * High Chairs Collapsible (selection-field)
 * High Charis Including Dinner Tray (selection-field)
 * High Chairs Material
 * Monitors Including Camera (selection-field)
 * Monitors Including 2-way voice operation (selection-field)
 * Monitors Maximum Range
 * Rockers Collapsible (selection-field)
 * Rockers Maximum Carry Weight
 * Strollers Number of Wheels
 * Textiles Size
 * Toys Age Category
 * Toys Type
 * Travelcots Collapsible (selection-field)
 * Travelcots Including Wheels (selection-field)
 * Travelcots Including Creep Hatch (selection-field)

Dependencies
==========

 * product_brand
 * mob_extra_images

How To Add More Attributes
==========================


Attributes with various options
-------------------------------
 
 * add attribute with correct code in Magento
 * add attribute as custom option in mob_brand/models/mob_synchronization.py
 * add attribute as custom option in selection field in babycare_product_brand/models/custom_option.py
 * add attribute as product_[custom option]_id in babycare_product_brand/models/product.py
 * add sync-button of custom option in babycare_product_brand/views/product_attributemanager.xml
 * add product_[custom option]_id in babycare_product_brand/views/product.xml (important: options="{'no_create': True}")
 * check translations of newly created attributes

Attributes with selection field
-------------------------------
 
 * add attribute with correct code in Magento including options (e.g.: yes/no, boy/girl, etc.)
 * add attribute as custom option in mob_brand/models/mob_synchronization.py
 * add attribute as product_[custom option] as selection field in babycare_product_brand/models/product.py
 * add product_[custom option] in babycare_product_brand/views/product.xml
 * check translations of newly created attributes

Known issues / Roadmap
======================

 * roadmap - add a field on all custom options to list the products on which the option is associated (like product brand)
 * roadmap - show a red ball icon/count badge on the attribute manager view behind the option type in case there are not synced custom options

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/babycarenl/babycare-odoo/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed feedback
`here <https://github.com/babycarenl/babycare-odoo/issues/new?body=module:%20babycare_product_brand%0Aversion:%208.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Credits
=======

This module is forked from the product_brand module of the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.
