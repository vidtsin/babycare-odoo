Sale customizations for Babycare
================================

* When a payment is registered for a sales order that is in state 'Shipping exception', the outgoing delivery is recreated
* In the POS interface, it is not possible to register payments larger than €10.000,-.
* Add a field for remarks on sales and purchase orders that are visible, but not editable, on the related delivery orders.
* Introduce end-of-life flag on product variants and keep in sync with product template state
* If a product is set to end-of-life, its Buy route is removed.
* If a product is end-of-life and has not been modified in three months, and it does not had any stock moves in that period, it gets deactivated.
* Add a clickable reference to SO or PO on picking. #1377
* Sale order line colors reflect the product status and expected stock level
* Purchase order line colors reflect the product status and expected stock level
* Picking line colors reflect the product status and expected stock level
* Sale orders are red in the list view if one of their products have a negative expected stock level (or are in an exception state, as red is the default color for that)
* Draft purchase orders are red in the list view if one of their products have a negative expected stock level (or are in an exception state, as red is the default color for that)
* Add product state 'Can be ordered'
* Remove product state 'Development'
* Sync Buy route with product state
* Set orderpoint qtys to zero in product state EOL, Obsolete and Can be ordered.
* Apply product colors to kanban view
* Allow product categories to be reordered in the category tree view
* For products created from the interface (not through import), minimum orderrules are created automatically
* No stock moves can be created from the standalone stock move view (for instance, referred to from the product form)
* Show supplier code on product variants
* Search supplier code, default code and EAN by default
* Rename product description to Long description and sale description to short description.
* Supplier invoices cannot be confirmed without a supplier invoice number filled in.
* Move fiscal position and payment term around on the supplier invoice form to make the latter more prominent
* Show a box button on the product and variant form views that opens the BOMS in which the product is a component
* Can search on products and variants whether it is a component
* Activate _parent_store for product public categories plus primary ordering by parent
* Implement a hierarchy view for public categories that link to products in those categories
* Prevent the removal of public categories that are still in use.
* Hide 'Invoice' button from pos order, which seems to create a redundant receivable accounting entry
* Add a field on the partner form to store the default purchase delay.
* Take the default purchase delay from the supplier when it is linked to a product (in the client and through product import)
* #2665, reroute messages from picking and invoice to the related sale order
* #2780, apply fiscal position based on the shipping address' country regardless of the customer's fiscal position
* Add a custom, stored definition of configurable products
* #2660, don't allow consumables with one attribute to be selected on a sale order line
* For configurable products, mask the default code on the template
* Introduce variant_published flag on the variant level (cf. template's website_published flag)
* Introduce variant_eol flag on the variant level (cf. template's eol/obsolete states)
* variant_published and variant_eol are kept in sync with nonconfigurable templates
* Introduce is_synced_magento flag on product to search on synced to Magento products
* Don't allow consumables with one attribute to be selected on an account invoice line
* Don't allow consumables with one attribute to be selected on a mrp bom line
* The warranty field on the product form is made invisible
* The volume and weight field on the product form are invisible
* #3245, Force product code and ean13 to be unique for non-configurable products
* #3344, added actions for automated emails for orders synchronized from Magento
* #3394, hide fax and title fields on customer views
* #3629, make ready and to do default in stock moves opened from the product form view