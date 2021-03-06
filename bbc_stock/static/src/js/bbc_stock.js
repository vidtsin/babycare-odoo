openerp.bbc_stock = function(instance){
    module = instance.stock;
    _t = instance.web._t;
    var QWeb   = instance.web.qweb;

    /* the stock wizard won't be initialized at this point, so we work on the
       prototype. That means extend instead of include. */

    module.PickingMainWidget = module.PickingMainWidget.extend({
        get_header: function(picking_id){
            var res = '';
            if(this.picking){
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

        done: function(){
            if (this.picking_editor.check_done()){
                this.barcode_notify('done');
            }
            else {
                this.barcode_notify('backorder');
            }
            var self = this;
            return this._super().then(function(res) {
                if (!res) {
                    return self.menu();
                }
                return res;
            });
        },

        load: function(picking_id){
            var self = this;
            var deferred = this._super(picking_id);
            deferred.then(
                function(){
                    if (self.picking) {
                        new instance.web.Model('magento.tracking.info').get_func('search_read')([['wk_picking_id', '=', parseInt(self.picking.id)]],[]).then(function(refs){
                            _.each(refs, function(ref){
                                $(QWeb.render('CarrierRef', {'ref': ref}))
                                    .insertBefore($('tr.input-carrier-ref'));
                            });
                        });
                    }
                }
            );
            return deferred;
        },

        scan: function(ean){ //scans a barcode, sends it to the server, then reload the ui
            /* Overwrite this function from core (addons/stock/static/src/widgets.js).
               We add in a notification if the product cannot be found.
               Additionally, we intercept a specific scanning code to trigger put-in-cart.
            */
            /* Start of additional local change that could have been done in an override */
            var ean_clean = ean.replace(/[\s\0]/, '');
            if (ean_clean === 'MKG') {
                return this.drop_down();
            }
            /* End of additional local change that could have been done in an override */
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
                    /* Start of local change */
                    if (result.sound) {
                        self.barcode_notify(result.sound);
                    }
                    /* End of local change */
                    if (result.operation_id !== false){
                        self.refresh_ui(self.picking.id).then(function(){
                            /* Start of local change */
                            if (result.done) {
                                self.$('#info_carrier_ref').focus();
                                self.barcode_notify('ready');
                            }
                            /* End of local change */
                            return self.picking_editor.blink(result.operation_id);
                        });
                    }
                });
        }
    });
    var PickingEditorWidgetSuper = module.PickingEditorWidget.prototype;
    module.PickingEditorWidget = module.PickingEditorWidget.extend({
        get_carrier: function() {
            var parent = this.getParent();
            if(parent.picking && parent.picking.carrier_id) {
                return parent.picking.carrier_id[1];
            }
        },
        get_address: function() {
            var parent = this.getParent();
            if(parent.picking.partner_address) {
                return parent.picking.partner_address;
            }
        },
        del_carrier_id: function(val) {
            var parent = this.getParent();
            if(parent.picking) {
                new instance.web.Model('magento.tracking.info')
                    .call('search', [
                        ['wk_picking_id', '=', parent.picking.id],
                        ['magento_carrier_tracking_ref', '=', val]],
                          {context: new instance.web.CompoundContext()});
            }
        },
        set_carrier_ref: function(val) {
            var parent = this.getParent();
            var self = this;
            if(parent.picking) {
                new instance.web.Model('magento.tracking.info')
                    .call('create', [{
                        'wk_picking_id': parent.picking.id,
                        'magento_carrier_tracking_ref': val}],
                          {context: new instance.web.CompoundContext()}).then(
                              function(new_id){
                                  $(QWeb.render('CarrierRef', {
                                          'ref': {'id': new_id,
                                                  'magento_carrier_tracking_ref': val}}))
                                      .insertBefore($('tr.input-carrier-ref'));
                              });
            }
            // TODO: set current line readonly. Create new line and focus.
        },
        get_remarks: function() {
            var parent = this.getParent();
            if(parent.picking.remarks) {
                return parent.picking.remarks;
            }
        },
        get_paid: function() {
            var parent = this.getParent();
            if(parent.picking) {
                return parent.picking.x_is_paid;
            }
        },
        /* Assign specific classes to rows with product not on the original
           picking, rows with insufficient or excessive amount and rows
           not scanned yet.

           Note that the Odoo js developer enjoyed thinking up new column names, such as
           'rem' for qty_done, presumably refering to 'remaining quantity'. However,
           the semantics of the field remained unchanged as 'scanned quantity'.

           Also, override sorting order imposed by the parent. In case of an associated
           package, we do not know the packop id, so we arbitrarily give them the highest
           position.
        */
        get_rows: function(){
            var result = PickingEditorWidgetSuper.get_rows.apply(this, arguments);
            var sorted = [];
            _.each(this.getParent().packoplines, function(line){
                sorted[line.id] = line.sequence;
            });
            result.sort(function(a, b){
                return (sorted[!a.package_id && a.cols.id] || 0) - (sorted[!b.package_id && b.cols.id] || 0);
            });
            _.each(result, function(row){
                if (!row.cols.qty) {
                    row.classes += 'unknown ';
                } else if (row.cols.rem && row.cols.qty != row.cols.rem) {
                    row.classes += 'incorrect ';
                }
            });
            return result;
        },
        renderElement: function() {
            this._super();
            var self = this;
            this.$('#info_carrier_ref').change(function(){
                var val = self.$('#info_carrier_ref').val();
                if (val){
                    if (val === 'MKG'){
                        return self.getParent().drop_down();
                    }
                    self.set_carrier_ref(self.$('#info_carrier_ref').val());
                    self.$('#info_carrier_ref').val('');
                    self.$('#info_carrier_ref').focus();
                }
            });

            // Prevent scanned carrier ref to be passed on as product code
            this.$('#info_carrier_ref').focus(function(){
                self.getParent().barcode_scanner.disconnect();
            });
            this.$('#info_carrier_ref').blur(function(){
                self.getParent().barcode_scanner.connect(function(ean){
                    self.getParent().scan(ean);
                });
            });
            self.$('table.carrier-refs').on('click', 'td.delete > button', function(){
                new instance.web.Model('magento.tracking.info')
                    .call('unlink', [[parseInt($(this).data('id'))]],
                          {context: new instance.web.CompoundContext()});
                $(this).parent().parent().remove();
            });
        }
    });
};
