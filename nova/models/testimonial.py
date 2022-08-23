from email.policy import default
from turtle import position
from pkg_resources import require
from odoo import models, fields, _
from odoo.exceptions import UserError


class Testimonial(models.Model):
    _name = 'nova.testimonial'
    _rec_name = 'first_name'
    _inherit = ['image.mixin']

    first_name = fields.Char('First Name')
    last_name = fields.Char('Last Name')
    image_1920 = fields.Image('Profile Image')
    position = fields.Char('Position')
    rate = fields.Selection(
        [('0', 'Zero'), ('1', 'One'), ('2', 'Two'), ('3', 'Three'), ('4', 'Four'),('5', 'Five')], default='0')
    comment = fields.Text('Comment')
