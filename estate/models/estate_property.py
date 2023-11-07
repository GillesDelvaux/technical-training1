from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from . import estate_property_type
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class estate_property(models.Model):
    _name = "estate.estate.property"
    _description = "Estate property model"

    name = fields.Char('Title', required=True)
    description = fields.Text('Description')
    postcode = fields.Char()
    date_availability = fields.Date('Available From',copy=False, default=lambda self: (fields.Date.context_today(self) +                    relativedelta(months=3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer('Living area(sqm)')
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    active = fields.Boolean(default=True)
    garden_area = fields.Integer('Garden area(sqm)')
    garden_orientation = fields.Selection(
        string = 'Garden Orientation',
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
    property_type_id = fields.Many2one('estate.estate.property.type', string = 'Property Type')
    user_id = fields.Many2one('res.users', string = 'Salesman', default=lambda self:self.env.user)
    partner_id = fields.Many2one('res.partner', string = 'Buyer', copy=False)
    tag_ids = fields.Many2many('estate.estate.property.tag')
    offers_ids = fields.One2many('estate.estate.property.offer', 'property_id')
    total_area = fields.Integer('Total area(sqm)',compute='_compute_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_offer')


    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Expected price should be stricly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling price should be stricly positive.')
    ]


    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area
    
    @api.depends('offers_ids.price')
    def _compute_best_offer(self):
        for record in self:
            if record.offers_ids:
                record.best_price = max(record.offers_ids.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden == True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False
        

    def action_property_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError("Canceled properties cannot be sold.")
            else:
                record.state = 'sold'
                return True
                
    def action_property_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            else:
                record.state = 'canceled'
                return True

    @api.constrains('expected_price', 'selling_price')
    def _check_price_difference(self):
        for record in self:
            if (
                not float_is_zero(record.selling_price, precision_rounding=0.01)
                and float_compare(record.selling_price, record.expected_price * 90.0 / 100.0, precision_rounding=0.01) < 0
            ):
                raise ValidationError("The selling price must be at least 90% of the expected price")
                   