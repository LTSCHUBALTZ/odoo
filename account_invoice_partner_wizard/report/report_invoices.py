# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################
#    Copyright (C) 2015 thinkasoft , C.A. (www.thinkasoft.com)
#    All Rights Reserved
# ############## Credits ######################################################
#    Developed by: thinkasoft , C.A.
#
#    Coded by:  Aular Hector Manuel (aular.hector3@gmail.com)
#
##############################################################################

import time
from openerp import api, models


class SaleMarginExtended(models.AbstractModel):

    _name = 'report.account_invoice_partner_wizard.report_invoices'

    @api.multi
    def render_html(self, data):
        active_model = self.env.context.get('active_model')

        if active_model == "account.invoice":
            invoice = self.env[active_model].browse(self.env.context.get('active_id'))
            docargs = {
                'doc_ids': [invoice.id],
                'doc_model': active_model,
                'data': data['form'],
                'docs': invoice,
                'time': time,
                'res_company_wizard': self.env['res.company'].browse(data['form']['information_company_id'][0]),
            }
            return self.env['report'].render('account_invoice_partner_wizard.report_invoices', docargs)
        if active_model == 'account.invoice.partner.wizard':
            wizard = self.env[active_model].browse(self.env.context.get('active_id'))
            invoice_id = self.env.context.get("params").get("id")
            invoice = self.env["account.invoice"].browse(invoice_id)
            data = {}
            data["form"] = invoice.read()[0]
            data["form"].update(
                wizard.read(
                    ['information_company_id', 'company_vat', 'company_city',
                    'company_street', 'company_street2', 'company_website',
                    'partner_id', 'partner_name', 'partner_vat', 'partner_city', 'partner_street',
                    'partner_street2', 'partner_website', 'state'
                    ])[0])
            docargs = {
                'doc_ids': [invoice.id],
                'doc_model': "account.invoice",
                'data': data['form'],
                'docs': invoice,
                'time': time,
                'res_company_wizard': self.env['res.company'].browse(data['form']['information_company_id'][0]),
            }
            return self.env['report'].render('account_invoice_partner_wizard.report_invoices', docargs)
