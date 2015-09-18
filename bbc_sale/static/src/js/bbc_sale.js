openerp.bbc_sale = function(instance) {
    var QWeb = instance.web.qweb,
    module = instance.point_of_sale,
    _t = instance.web._t;

    /*
      When a product is scanned in the payment widget, the numeric product code
      is interpreted as the paid amount and the order is validated. For that reason,
      block here if a rather large amount is entered.
      NB. POS has not been initialized at this point, so we work on the prototype.
      That means extend instead of include, but it should not be harmful.
    */

    var validate_order_super = module.PaymentScreenWidget.prototype.validate_order;
    module.PaymentScreenWidget = module.PaymentScreenWidget.extend({
        validate_order: function(options) {
            var currentOrder = this.pos.get('selectedOrder');
            var plines = currentOrder.get('paymentLines').models;
            for (var i = 0; i < plines.length; i++) {
                if (plines[i].get_amount() > 10000) {
                    this.pos_widget.screen_selector.show_popup('error',{
                        message: _t('Payment contains an invalid amount'),
                        comment: _t('An amount higher than €10.000 has been entered as a payment. Please check this amount.'),
                    });
                    return;
                }
            }
            return validate_order_super.call(this, options);
        }
    });
}
