# -*- coding: utf-8 -*-
from openerp import api
from openerp.addons.product_brand.product_brand import (
    ProductProduct, ProductTemplate)


@api.multi
def product_name_get(self):
    return super(ProductProduct, self).name_get()


@api.multi
def template_name_get(self):
    return super(ProductTemplate, self).name_get()


def post_load():
    """ Monkeypatch the replacement methods onto the models from
    the product_brand module when this module is loaded """
    ProductProduct.name_get = product_name_get
    ProductTemplate.name_get = template_name_get
