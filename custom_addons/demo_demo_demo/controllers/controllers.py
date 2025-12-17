# -*- coding: utf-8 -*-
# from odoo import http


# class DemoDemoDemo(http.Controller):
#     @http.route('/demo_demo_demo/demo_demo_demo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/demo_demo_demo/demo_demo_demo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('demo_demo_demo.listing', {
#             'root': '/demo_demo_demo/demo_demo_demo',
#             'objects': http.request.env['demo_demo_demo.demo_demo_demo'].search([]),
#         })

#     @http.route('/demo_demo_demo/demo_demo_demo/objects/<model("demo_demo_demo.demo_demo_demo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('demo_demo_demo.object', {
#             'object': obj
#         })

