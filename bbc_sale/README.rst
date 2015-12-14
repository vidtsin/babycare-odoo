Sale customizations for Babycare
================================

* When a payment is registered for a sales order that is in state 'Shipping exception', the outgoing delivery is recreated
* In the POS interface, it is not possible to register payments larger than €10.000,-.
* Add a field for remarks on sales and purchase orders that are visible, but not editable, on the related delivery orders.
* If a product is set to end-of-life, its Buy route is removed.
* If a product is end-of-life and has not been modified in three months, and it does not had any stock moves in that period, it gets deactivated.
* Add a clickable reference to SO or PO on picking. #1377
* Sale order line colors reflect the product status and expected stock level
* Purchase order line colors reflect the product status and expected stock level
* Picking line colors reflect the product status and expected stock level
* Sale orders are red in the list view if one of their products have a negative expected stock level (or are in an exception state, as red is the default color for that)
* Draft purchase orders are red in the list view if one of their products have
a negative expected stock level (or are in an exception state, as red is the default color for that)
* Add product state 'Can be ordered'
* Remove product state 'Development'
* Sync Buy route with product state
* Set orderpoint qtys to zero in product state EOL, Obsolete and Can be ordered.
* Apply product colors to kanban view
* Allow product categories to be reordered in the category tree view
* For products created from the interface (not through import), minimum orderrules are created automatically
