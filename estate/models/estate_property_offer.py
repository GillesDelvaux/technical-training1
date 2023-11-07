from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from datetime import date


class estate_property_offer(models.Model):
    _name = "estate.estate.property.offer"
    _description = "Estate property offer model"
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'An offer price should be stricly positive.')
    ]
    
    price = fields.Float()
    status = fields.Selection(
        string = 'Status',
        selection = [('accepted','Accepted'),('refused','Refused')],
        copy = False)
    partner_id = fields.Many2one('res.partner', required = True)
    property_id = fields.Many2one('estate.estate.property', required = True)
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')


    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)
            else:
                record.date_deadline = date.today() + relativedelta(days=record.validity)
            
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - date.today()).days

    def property_offer_accept(self):
        for record in self:
            if record.property_id.state == 'offer_accepted' or record.property_id.state == 'sold':
                 raise UserError("Property already sold or an offer has been accepted already")
            else:
                record.status = 'accepted'
                record.property_id.selling_price = record.price 
                record.property_id.partner_id = record.partner_id
                record.property_id.state = 'offer_accepted'
                return True    

    def property_offer_refuse(self):
        for record in self:
            record.status = 'refused'
            return True  