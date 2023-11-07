from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class estate_property_offer(models.Model):
    _name = "estate.estate.property.offer"
    _description = "Estate property offer model"

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
                record.date_deadline =Date.today() + relativedelta(days=record.validity)
            
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - Date.today()).days
            
            