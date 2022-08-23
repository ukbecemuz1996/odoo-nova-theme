from datetime import datetime
from email.policy import default
from operator import index
from odoo import api, models, fields, _
from odoo.exceptions import UserError


class Post(models.Model):
    _name = 'nova.blog.post'
    _inherit = ['image.mixin']
    _rec_name = 'title'

    title = fields.Char('Title')
    user_id = fields.Many2one(
        'res.users', string='Writer')
    date = fields.Date('Date', default=datetime.today())
    image_1920 = fields.Image('Cover Image')
    category_id = fields.Many2one('nova.blog.category', 'Post Category')
    tag_ids = fields.Many2many('nova.blog.tag', string='Post Tags')
    content = fields.Html('Content')

    @api.model
    def create(self, vals):
        if not vals.get('user_id'):
            vals['user_id'] = self.env.uid
        return super().create(vals)

    def write(self, vals):
        if 'user_id' in vals:
            if not vals.get('user_id'):
                vals['user_id'] = self.env.uid
        write_move = super(Post, self).write(vals)
        return write_move

    @api.model
    def recent_posts(self,limit):
        return self.env['nova.blog.post'].search([],order='date desc',limit=limit)


class PostCategory(models.Model):
    _name = 'nova.blog.category'
    _rec_name = 'name'

    name = fields.Char('Name')
    posts_count = fields.Integer('Posts Count', compute="_compute_posts_count")
    post_ids = fields.One2many('nova.blog.post', 'category_id', string='Posts')

    @api.depends('post_ids')
    def _compute_posts_count(self):
        for record in self:
            record.posts_count = len(record.post_ids)


class PostTag(models.Model):
    _name = 'nova.blog.tag'
    _rec_name = 'name'

    name = fields.Char('Name')
