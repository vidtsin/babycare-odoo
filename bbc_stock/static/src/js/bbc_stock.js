openerp.bbc_stock = function(instance){
    module = instance.stock,
    _t = instance.web._t;

    /* the stock wizard won't be initialized at this point, so we work on the
       prototype. That means extend instead of include. */

    module.PickingMainWidget = module.PickingMainWidget.extend({
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
        },

    });
}
