from pkg_resources import require
from odoo import models, fields, _
from odoo.exceptions import UserError


class TeamPosition(models.Model):
    _name = 'nova.team.position'
    _rec_name = 'name'

    name = fields.Char('Position')


class Team(models.Model):
    _name = 'nova.team'
    _rec_name = 'first_name'
    _inherit = ['image.mixin']

    first_name = fields.Char('First Name')
    last_name = fields.Char('Last Name')
    image_1920 = fields.Image('Profile Image')
    twitter_link = fields.Char('Twitter')
    facebook_link = fields.Char('Facebook')
    instagram_link = fields.Char('Instagram')
    linkedin_link = fields.Char('Linkedin')
    position_id = fields.Many2one('nova.team.position', 'Position')
