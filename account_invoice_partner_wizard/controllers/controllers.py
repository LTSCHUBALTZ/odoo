# -*- coding: utf-8 -*-
from openerp import http

# class AccountInvoiceRicardo(http.Controller):
#     @http.route('/account_invoice_ricardo/account_invoice_ricardo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_invoice_ricardo/account_invoice_ricardo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_invoice_ricardo.listing', {
#             'root': '/account_invoice_ricardo/account_invoice_ricardo',
#             'objects': http.request.env['account_invoice_ricardo.account_invoice_ricardo'].search([]),
#         })

#     @http.route('/account_invoice_ricardo/account_invoice_ricardo/objects/<model("account_invoice_ricardo.account_invoice_ricardo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_invoice_ricardo.object', {
#             'object': obj
#         })