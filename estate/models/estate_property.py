from dateutil.relativedelta import relativedelta
from odoo import fields, models

class estate_property(models.Model):
    _name = "estate.estate.property"
    _description = "Estate property model"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: (fields.Date.context_today(self) + relativedelta(months=3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string = 'Orientation',
        selection = [('north', 'North'), ('south','South'),('east','East'),('west','West')],
        help = "This is used to get the orientation of the garden"
    )
    state = fields.Selection(
        string = 'State',
        selection = [('new', 'New'), ('offer_received','Offer Received'),('offer_accepted','Offer Accepted'),('sold','Sold'),                           ('canceled','Canceled')],
        required=True,
        copy=False,
        default='new'
    )



