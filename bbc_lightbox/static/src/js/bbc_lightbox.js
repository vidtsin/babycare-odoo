openerp.bbc_lightbox = function (instance) {
    instance.web.form.FieldBinaryImage.include({
        render_value: function() {
            this._super.apply(this, arguments);
            var img = this.$el.find('img')[0];
            $(img).unbind('click');
            var self = this;
            $(img).click(function(e) {
                if(self.view.get("actual_mode") == "view") {
                    var parent = self.getParent();
                    var field = img.name;
                    if (img.name === 'image_medium' || img.name === 'image_small') {
                        field = 'image'
                    }
                    url = '/web/binary/image?model=' + parent.dataset.model + '&amp;field=' + field + '&amp;id=' + parent.datarecord.id;
                    $.featherlight(img, {'image': url});
                    e.stopPropagation();
                }
            });
        },
    });
}
