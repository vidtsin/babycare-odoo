Stock customizations for Babycare
=================================

Barcode interface
-----------------
* Open in a new window
* Display order number, delivery address, tracking info and remarks, and sale order paid status
* Add or delete multiple Magento tracking references. This will update the number of packages on the picking.

The tracking reference field will be set to focus after the last of the expected products has been scanned on a customer bound shipment

Lines are ordered, and colored as follows:
* lines with products that do not have a corresponding line in the current picking (Red)
* incomplete or overcomplete lines (Yellow)
* lines with products that have not yet been scanned (White)
* lines that are satisfied (Green)

A special scan code 'MKG' triggers put-in-cart. Afterwards, the menu will be shown instead of moving on to the next picking.

Different sounds play on
* Scanning unknown code
* Scanning unrelated product or excessive amount
* Scanning an expected product
* Put in cart
* Make a backorder

TODO: unscanned products stay on top even if there are red and yellow lines.

* When scanning products in the barcode interface, consumable products with a single product attribute (as defined in the bbc_sale module) are ignored.

Other functionality
===================
* Add a field to the product form that displays the maximum delivery date for all of the incoming stock. A manual override can be entered. This override will be reset when the override date is reached, or when there is actually stock incoming.
* Menu shortcuts to late deliveries to and from customers or from suppliers. This changes the cutoff time of the 'late' filter on pickings to start of the day (in UTC).
* Hide the stock locations group on the product form
* Hide the lot tracking group on the product form
* #2660, don't allow consumables with more than one attribute to be selected on a manually created stock move
* Disable create and edit function and filter on is_synced_magento == True for the fields under the website group on the product form
* Hide style and sequence fields under the website group on the product form
* #2800, show move lines' expected dates in the picking lines. Show max expected date on the picking. Max date is writeable and resets the moves' expected dates.
* Picking's max_date, and move's date_expected are rendered as date instead of timestamp fields.

Credits
-------

Audio files from Flashkit

* Unknown barcode: http://www.flashkit.com/imagesvr_ce/flashkit/soundfx/Interfaces/Beeps/Alarm_Hi-Adam_A_-8903/Alarm_Hi-Adam_A_-8903_hifi.mp3

Audio file from Freesound:
* Ready to deliver: https://freesound.org/people/philitup321/sounds/204369/
