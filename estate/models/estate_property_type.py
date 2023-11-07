from odoo import fields, models

class estate_property_type(models.Model):
    _name = "estate.estate.property.type"
    _description = "Estate property type model"

    name = fields.Char('Property type', required=True)
    