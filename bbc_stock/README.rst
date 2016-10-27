Stock customizations for Babycare
=================================

Barcode interface
-----------------
* Open in a new window
* Display order number, delivery address, tracking info and remarks, and sale order paid status
* Tracking reference is editable

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

Other functionality
===================
Add a field to the product form that displays the maximum delivery date for all of the incoming stock.

Credits
-------

Audio files from Flashkit

* Unknown barcode: http://www.flashkit.com/imagesvr_ce/flashkit/soundfx/Interfaces/Beeps/Alarm_Hi-Adam_A_-8903/Alarm_Hi-Adam_A_-8903_hifi.mp3

Audio file from Freesound:
* Ready to deliver: https://freesound.org/people/philitup321/sounds/204369/
