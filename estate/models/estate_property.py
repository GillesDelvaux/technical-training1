from odoo import fields, models

class estate_property(models.Model):
    _name = "estate.estate.property"
    _description = "Estate property model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string =  'Orientation',
        selection = [('north', 'North'), ('south','South'),('east','East'),('west','West')],
        help = "This is used to get the orientation of the garden"
    )
