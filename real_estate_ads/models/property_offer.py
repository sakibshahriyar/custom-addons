from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'), ('refused', 'Refused')], string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity")
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')

    _sql_constraints = [
        ('check_validity', 'CHECK(validity > 0)','Deadline must be greater than Creation Date')
    ]

    creation_date = fields.Date(string="Creation Date")

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.today()
        return super(PropertyOffer, self).create(vals)

    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise ValidationError("Deadline must be greater than Creation Date")

    def write(self, vals):
        print(vals)
        res_partner_ids = self.env['res.partner'].search_count([
            ('is_company', '=', True),
        ])
        print(res_partner_ids)
        return super(PropertyOffer,self).write(vals)
    # def write(self, vals):
    #     # Check if 'is_partner' is a valid field on 'res.partner' model
    #     if 'res.partner' in self.env and 'is_company' in self.env['res.partner']._fields:
    #         # Perform the search count operation
    #         res_partner_ids = self.env['res.partner'].search_count([
    #             ('is_company', '=', True),
    #         ])
    #         print(res_partner_ids)
    #     else:
    #         print("Field 'is_partner' not found on 'res.partner' model.")
    #
    #     return super(PropertyOffer, self).write(vals)

