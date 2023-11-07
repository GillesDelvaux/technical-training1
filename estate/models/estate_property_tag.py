from odoo import fields, models

class estate_property_tag(models.Model):
    _name = "estate.estate.property.tag"
    _description = "Estate property tag model"
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'A tag must be unique.')
    ]

    name = fields.Char('Property tag', required=True)
    