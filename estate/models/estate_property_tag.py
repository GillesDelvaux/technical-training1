from odoo import fields, models

class estate_property_tag(models.Model):
    _name = "estate.estate.property.tag"
    _description = "Estate property tag model"

    name = fields.Char('Property tag', required=True)
    