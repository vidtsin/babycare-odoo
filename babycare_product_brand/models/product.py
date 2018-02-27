# -*- coding: utf-8 -*-
from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_color_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'color')],
        context={'default_option_type': 'color'},
        string="Color"
    )
    product_warranty_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'warranty')],
        context={'default_option_type': 'warranty'},
        string="Warranty (Attribute Manager)"
    )
    product_buggies_agecategory_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'buggies.agecategory')],
        context={'default_option_type': 'buggies.agecategory'},
        string="Age Category (Buggies)"
    )
    product_buggies_maxcarryweight_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'buggies.maxcarryweight')],
        context={'default_option_type': 'buggies.maxcarryweight'},
        string="Maximum Carry Weight (Buggies)"
    )
    product_buggies_numberofwheels_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'buggies.numberofwheels')],
        context={'default_option_type': 'buggies.numberofwheels'},
        string="Number of Wheels (Buggies)"
    )
    product_carriers_directionofuse_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'carriers.directionofuse')],
        context={'default_option_type': 'carriers.directionofuse'},
        string="Direction of Use (Carriers)"
    )
    product_carriers_maxcarryweight_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'carriers.maxcarryweight')],
        context={'default_option_type': 'carriers.maxcarryweight'},
        string="Maximum Carry Weight (Carriers)"
    )
    product_carriers_type_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'carriers.type')],
        context={'default_option_type': 'carriers.type'},
        string="Type (Carriers)"
    )
    product_carseats_agecategory_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'carseats.agecategory')],
        context={'default_option_type': 'carseats.agecategory'},
        string="Age Category (Car Seats)"
    )
    product_carseats_childlength_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'carseats.childlength')],
        context={'default_option_type': 'carseats.childlength'},
        string="Child Length (Car Seats)"
    )
    product_carseats_childweight_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'carseats.childweight')],
        context={'default_option_type': 'carseats.childweight'},
        string="Child Weight (Car Seats)"
    )
    product_carseats_directionofuse_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'carseats.directionofuse')],
        context={'default_option_type': 'carseats.directionofuse'},
        string="Direction of Use (Car Seats)"
    )
    product_carseats_installmethod_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'carseats.installmethod')],
        context={'default_option_type': 'carseats.installmethod'},
        string="Install Method (Car Seats)"
    )
    product_clothes_season_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'clothes.season')],
        context={'default_option_type': 'clothes.season'},
        string="Season (Clothes)"
    )
    product_clothes_size_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'clothes.size')],
        context={'default_option_type': 'clothes.size'},
        string="Size (Clothes)"
    )
    product_highchairs_agecategory_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'highchairs.agecategory')],
        context={'default_option_type': 'highchairs.agecategory'},
        string="Age Category (High Chairs)"
    )
    product_highchairs_material_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'highchairs.material')],
        context={'default_option_type': 'highchairs.material'},
        string="Material (High Chairs)"
    )
    product_monitors_maxrange_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'monitors.maxrange')],
        context={'default_option_type': 'monitors.maxrange'},
        string="Maximum Range (Monitors)"
    )
    product_rockers_maxcarryweight_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'rockers.maxcarryweight')],
        context={'default_option_type': 'rockers.maxcarryweight'},
        string="Maximum Carry Weight (Rockers)"
    )
    product_strollers_numberofwheels_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'strollers.numberofwheels')],
        context={'default_option_type': 'strollers.numberofwheels'},
        string="Number of Wheels (Strollers)"
    )
    product_textiles_size_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'textiles.size')],
        context={'default_option_type': 'textiles.size'},
        string="Size (Textiles)"
    )
    product_toys_agecategory_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'toys.agecategory')],
        context={'default_option_type': 'toys.agecategory'},
        string="Age Category (Toys)"
    )
    product_toys_type_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'toys.type')],
        context={'default_option_type': 'toys.type'},
        string="Type (Toys)"
    )
    product_buggies_adjustablebackrest = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Adjustable Backrest? (Buggies)"
    )
    product_clothes_gender = fields.Selection(
        [('boy', 'Boy'), ('girl', 'Girl'), ('unisex', 'Unisex')],
        string="Gender (Clothes)"
    )
    product_highchairs_includingdinnertray = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Including Dinner Tray (High Chairs)"
    )
    product_highchairs_collapsible = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Collapsible (High Chairs)"
    )
    product_monitors_includingcamera = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Including Camera (Monitors)"
    )
    product_monitors_includingrecallfunction = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="2-way voice operation (Monitors)"
    )
    product_rockers_collapsible = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Collapsible (Rockers)"
    )
    product_travelcots_collapsible = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Collapsible (Travelcots)"
    )
    product_travelcots_includingwheels = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Including Wheels (Travelcots)"
    )
    product_travelcots_includingcreephatch = fields.Selection(
        [('yes', 'Yes'), ('no', 'No')],
        string="Including Creep Hatch (Travelcots)"
    )


class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_color_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'color')],
        context={'default_option_type': 'color'},
        string="Color"
    )
    product_clothes_size_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'clothes.size')],
        context={'default_option_type': 'clothes.size'},
        string="Size (Clothes)"
    )
    product_textiles_size_id = fields.Many2one(
        'custom.option',
        domain=[('option_type', '=', 'textiles.size')],
        context={'default_option_type': 'textiles.size'},
        string="Size (Textiles)"
    )

    @api.multi
    def open_attribute_manager(self):
        res = {
            'type': 'ir.actions.act_window',
            'name': 'Attribute Manager',
            'res_model': 'product.attributemanager',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'self',
            'flags': {'action_buttons': False},
        }
        return res
