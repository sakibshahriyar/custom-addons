from odoo import fields, models, api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'

    name = fields.Char(string='Name', required=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    type_id = fields.Many2one('estate.property.type', string='Property Type')
    description = fields.Char(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Available From', readonly=True)
    expected_price = fields.Float(string='Expected Price')
    best_offer = fields.Float(string='Best Offer')
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer(string='Bedrooms')
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Facades')
    garages = fields.Integer(string='Garages', default=False)
    garden = fields.Integer(string='Garden', default=False)
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')], string='Garden Orientation')

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")
    sales_id = fields.Many2one('res.users', string='Salesman')
    buyer_id = fields.Many2one('res.partner', string='Buyer', domain=[('is_company', '=', True)])
    phone = fields.Char(string="Phone", related='buyer_id.phone')

    @api.onchange('living_area', 'garden_area')
    def _onchange_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    total_area = fields.Integer(string='Total Area')

    @api.constrains('total_area')
    def _check_total_area(self):
        for rec in self:
            if rec.total_area <= 0:
                raise ValidationError("Total area must be a positive integer.")


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'
    name = fields.Char(string='Name', required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'

    name = fields.Char(string='Name', required=True)

