from datetime import datetime
from operator import index
from odoo import api,models, fields, _
from odoo.exceptions import UserError


class Project(models.Model):
    _name = 'nova.project'
    _rec_name = 'title'

    title = fields.Char('Title')
    description = fields.Text('Description')
    url = fields.Char('URL')
    date = fields.Date('Date', default=datetime.today())
    client = fields.Char('Client')
    cover_image = fields.Image('Cover Image')
    category_id = fields.Many2one('nova.project.category', 'Project Category')
    tag_ids = fields.Many2many('nova.project.tag', string='Project Tags')
    tag_ids_class = fields.Char(compute='_compute_filter_classes')
    project_image_ids = fields.One2many(
        'nova.project.image', 'project_id', string='Extra Project Images', copy=True)
    website_url = fields.Char(compute='_compute_website_url',store=True)

    def _compute_filter_classes(self):
        for record in self:
            classes = ''
            for tag in record.tag_ids:
                classes += ' filter-'+tag.name
            record.tag_ids_class = classes

    @api.depends("title")
    def _compute_website_url(self):
        for record in self:
            if record.title:
                website_url = record.title.lower().replace(" ", "-")
                all_urls = self.env['nova.project'].search(
                    [('website_url', '=', website_url)])
                if all_urls:
                    website_url += "-" + str(record.id)

                record.website_url = website_url


class ProjectImage(models.Model):
    _name = 'nova.project.image'
    _inherit = ['image.mixin']

    image_1920 = fields.Image(required=True)
    project_id = fields.Many2one(
        'nova.project', 'Project', index=True, ondelete='cascade')


class ProjectCategory(models.Model):
    _name = 'nova.project.category'
    _rec_name = 'name'

    name = fields.Char('Name')


class ProjectTag(models.Model):
    _name = 'nova.project.tag'
    _rec_name = 'name'

    name = fields.Char('Name')
