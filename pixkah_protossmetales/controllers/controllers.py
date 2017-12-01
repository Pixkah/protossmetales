# -*- coding: utf-8 -*-
from odoo import http

# class PixkahProtossmetales(http.Controller):
#     @http.route('/pixkah_protossmetales/pixkah_protossmetales/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pixkah_protossmetales/pixkah_protossmetales/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pixkah_protossmetales.listing', {
#             'root': '/pixkah_protossmetales/pixkah_protossmetales',
#             'objects': http.request.env['pixkah_protossmetales.pixkah_protossmetales'].search([]),
#         })

#     @http.route('/pixkah_protossmetales/pixkah_protossmetales/objects/<model("pixkah_protossmetales.pixkah_protossmetales"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pixkah_protossmetales.object', {
#             'object': obj
#         })