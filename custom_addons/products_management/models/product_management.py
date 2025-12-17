from odoo import models, fields

class ProductManagement(models.Model):
    _name = 'product.management'
    _description = 'Product Management Model'
    name = fields.Char(string='Product Name', required=True)
    description = fields.Text(string='Product Description')
    price = fields.Float(string='Product Price', required=True)
    available_quantity = fields.Integer(string='Available Quantity', default=0)