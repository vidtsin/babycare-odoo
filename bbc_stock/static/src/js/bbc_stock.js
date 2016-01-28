openerp.bbc_stock = function(instance){
    module = instance.stock,
    _t = instance.web._t;

    /* the stock wizard won't be initialized at this point, so we work on the
       prototype. That means extend instead of include. */

    module.PickingMainWidget = module.PickingMainWidget.extend({
        get_header: function(picking_id){
            var res = '';
            if(this.picking){
                if(this.picking.partner_id) {
                    // Render the delivery address
                    var ctx = new instance.web.CompoundContext();
                    ctx.add({'show_address': 1});
                    var self = this
                    var address = new instance.web.Model("res.partner").call(
                        'name_get', [[this.picking.partner_id[0]], ctx]).then(function(result) {
                            self.$('#address').text(result[0][1]);
                        });
                }
                res = this.picking.name;
                if(this.picking.origin){
                    // Append the pickings origin to the header text
                    res = res + ' - ' + this.picking.origin.split(":")[0];
                }
            }
            return res;
        },

        barcode_notify: function(mode) {
            // play a sound depending on the mode
            var audio = new Audio('/bbc_stock/static/src/snd/' + mode + '.mp3');
            audio.play();
        },

        scan: function(ean){ //scans a barcode, sends it to the server, then reload the ui
            /* Overwrite this function from core (addons/stock/static/src/widgets.js).
               We add in a notification if the product cannot be found */
            var self = this;
            var product_visible_ids = this.picking_editor.get_visible_ids();
            return new instance.web.Model('stock.picking')
                .call('process_barcode_from_ui', [self.picking.id, ean, product_visible_ids])
                .then(function(result){
                    if (result.filter_loc !== false){
                        //check if we have receive a location as answer
                        if (result.filter_loc !== undefined){
                            var modal_loc_hidden = self.$('#js_LocationChooseModal').attr('aria-hidden');
                            if (modal_loc_hidden === "false"){
                                var line = self.$('#js_LocationChooseModal .js_loc_option[data-loc-id='+result.filter_loc_id+']').attr('selected','selected');
                            }
                            else{
                                self.$('.oe_searchbox').val(result.filter_loc);
                                self.on_searchbox(result.filter_loc);
                            }
                        }
                    }
                    if (result.operation_id !== false){
                        self.refresh_ui(self.picking.id).then(function(){
                            return self.picking_editor.blink(result.operation_id);
                        });
                    }
                    /* Start of local change */
                    else {
                        self.barcode_notify('unknown');
                    }
                    /* End of local change */
                });
        }
    });
    var PickingEditorWidgetSuper = module.PickingEditorWidget.prototype;
    module.PickingEditorWidget = module.PickingEditorWidget.extend({
        /* Assign specific classes to rows with product not on the original
           picking, rows with insufficient or excessive amount and rows
           not scanned yet.

           Note that the Odoo js developer enjoyed thinking up new column names, such as
           'rem' for qty_done, presumably refering to 'remaining quantity'. However,
           the semantics of the field remained unchanged as 'scanned quantity'.
        */
        get_rows: function(){
            var result = PickingEditorWidgetSuper.get_rows.apply(this, arguments);
            _.each(result, function(row){
                if (!row.cols.qty) {
                    row.classes += 'unknown ';
                    console.log(row.cols.id + 'unknown');
                } else {
                    if (!row.cols.rem) {
                        console.log(row.cols.id + 'not scanned');
                    } else {
                        if (row.cols.qty != row.cols.rem) {
                            row.classes += 'incorrect ';
                            console.log(row.cols.id + 'qty not equal');
                        }
                    }
                }
            });
            return result;
        }
    });
}
