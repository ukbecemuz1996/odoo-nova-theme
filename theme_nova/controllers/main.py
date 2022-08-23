from odoo import http

from werkzeug.exceptions import Forbidden, NotFound


class Nova(http.Controller):

    @http.route('/', auth='public', website=True)
    def home(self, **kw):

        # recent posts
        recent_posts = http.request.env['nova.blog.post'].recent_posts(4)
        values = {
            'recent_posts': recent_posts,
        }
        return http.request.render('theme_nova.nova_homepage', values)

    @http.route('/portfolios', auth='public', website=True)
    def portfolios(self, **kw):

        tags = http.request.env['nova.project.tag'].search([])
        projects = http.request.env['nova.project'].search([])
        values = {
            'tags': tags,
            'projects': projects
        }
        return http.request.render('theme_nova.portfolios', values)

    @http.route('/portfolios/<permalink>', auth='public', website=True)
    def portfolio(self, permalink):
        project = http.request.env['nova.project'].search(
            [('website_url', '=', permalink)], limit=1)
        if not project:
            return http.request.not_found()
        values = {
            'project': project
        }
        return http.request.render('theme_nova.portfolio', values)

    @http.route('/team', auth='public', website=True)
    def team(self, **kw):

        team = http.request.env['nova.team'].search([])
        values = {
            'team': team,
        }
        return http.request.render('theme_nova.team', values)

    @http.route('/about', auth='public', website=True)
    def about(self, **kw):

        team = http.request.env['nova.team'].search([])
        values = {
            'team': team,
        }
        return http.request.render('theme_nova.about_us', values)

    @http.route('/services', auth='public', website=True)
    def services(self, **kw):

        testimonials = http.request.env['nova.testimonial'].search([])
        values = {
            'testimonials': testimonials,
        }
        return http.request.render('theme_nova.services', values)

    @http.route([
        '''/blog''',
        '''/blog/page/<int:page>''',
        '''/blog/category/<int:category_id>''',
        '''/blog/category/<int:category_id>/page/<int:page>''',
        '''/blog/tag/<int:tag_id>''',
        '''/blog/tag/<int:tag_id>/page/<int:page>''',
        '''/blog/post/<int:post_id>''',
        '''/blog/search/<q>''',
        '''/blog/search/<q>/page/<int:page>''',
    ], auth='public', website=True)
    def blog(self, page=1, category_id=-1, tag_id=-1, post_id=-1, q=None, **kw):

        post = None
        category = None
        tag = None
        if post_id != -1:
            post = http.request.env['nova.blog.post'].search(
                [('id', '=', post_id)])
            if not post:
                raise NotFound()

        # tags
        tags = http.request.env['nova.blog.tag'].search(
            [], limit=10)

        # posts
        offset = ((page - 1) * 10)
        limit = 10
        posts_search = []
        if q:
            posts_search.append(('title', 'like', q))
        if category_id != -1:
            category = http.request.env['nova.blog.tag'].search(
                [('id', '=', category_id)])
            if not category:
                raise NotFound()
            posts_search.append(('category_id', '=', category_id))
        if tag_id != -1:
            tag = http.request.env['nova.blog.tag'].search(
                [('id', '=', tag_id)])
            if not tag:
                raise NotFound()
            posts_search.append(('tag_ids', 'in', (tag_id)))

        posts = http.request.env['nova.blog.post'].search(
            posts_search, offset=offset, limit=limit)
        # categories
        cats_search = [('post_ids', 'in', posts.ids)]
        categories = http.request.env['nova.blog.category'].search([])
        # recent posts
        resent_posts = http.request.env['nova.blog.post'].recent_posts(6)
        # post pager
        posts_count = posts.search_count(posts_search)
        pager_url = None
        if category_id != -1:
            pager_url = "/blog/category/"+str(category_id)
        elif tag_id != -1:
            pager_url = "/blog/tag/"+str(tag_id)
        elif q:
            pager_url = "/blog/search/"+q
        else:
            pager_url = "/blog"

        pager = http.request.website.pager(
            url=pager_url,
            total=posts_count,
            page=page,
            step=10
        )
        values = {
            'post': post,
            'posts': posts,
            'category': category,
            'categories': categories,
            'resent_posts': resent_posts,
            'tag': tag,
            'tags': tags,
            'pager': pager,
            'q': q
        }
        return http.request.render('theme_nova.blog', values)
