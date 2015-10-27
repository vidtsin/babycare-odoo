Sale customizations for Babycare
================================

* When a payment is registered for a sales order that is in state 'Shipping
exception', the outgoing delivery is recreated
* In the POS interface, it is not possible to register payments larger than
€10.000,-.
* Add a field for remarks on sales and purchase orders that are visible, but
not editable, on the related delivery orders.
* If a product is set to end-of-life, its Buy route is removed.
* If a product is end-of-life and has not been modified in three months, and
it does not had any stock moves in that period, it gets deactivated.
* Add a clickable reference to SO or PO on picking. #1377
* Lines on sale orders reflect the product status and expected stock level
* Sale orders are red if one of their products have a negative expected stock
level (or are in an exception state, as red is the default color for that)
