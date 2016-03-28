openerp.bbc_lightbox = function (instance) {
    instance.web.form.FieldBinaryImage.include({
        render_value: function() {
            this._super.apply(this, arguments);
            var img = this.$el.find('img')[0];
            $(img).unbind('click');
            var self = this;
            $(img).click(function(e) {
                if(self.view.get("actual_mode") == "view") {
                    $.featherlight(img, {'image': 'http://www.geenstijl.nl/archives/images/brilvrouw.png'});
                    e.stopPropagation();
                }
            });
        },
    });
}
