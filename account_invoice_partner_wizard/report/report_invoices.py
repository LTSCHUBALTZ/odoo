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

import calendar
import datetime
import time
from openerp import api, models


class SaleMarginExtended(models.AbstractModel):

    _name = 'report.account_invoice_partner_wizard.report_invoices'

    @api.model
    def _set_date_literal(self, data):
        # Literal date
        string_date = data["form"].get("date_invoice")
        date = datetime.datetime.strptime(string_date, "%Y-%M-%d")
        position = date.month
        month = calendar.month_name[position].capitalize()
        date_final = "%s %s %s" % (date.day, month, date.year)
        data["form"].update({"date_literal": date_final})

    @api.model
    def _set_control_code(self, wizard, invoice, data):
        # Code
        control_code_simple = invoice._get_control_code(
            wizard.information_company_id.account_key,
            wizard.partner_id)
        data["form"].update({"control_code_simple": control_code_simple})
        control_code = invoice._get_control_code_final(
            control_code_simple,
            data["form"].get("company_vat"),
            data["form"].get("partner_vat"),
        )
        data["form"].update({"control_code": control_code})

    @api.multi
    def render_html(self, data):
        active_model = self.env.context.get('active_model')

        if active_model == "account.invoice":
            invoice = self.env[active_model].browse(self.env.context.get('active_id'))
            wizard = self.env["account.invoice.partner.wizard"].browse(
                self.env.context.get('active_ids')[0])

            data["form"].update(
                wizard.read(
                    ['information_company_id', 'company_vat', 'company_city',
                    'company_street', 'company_street2', 'company_website',
                    'partner_id', 'partner_name', 'partner_vat', 'partner_city', 'partner_street',
                    'partner_street2', 'partner_website', 'state'
                    ])[0])

            self._set_date_literal(data)
            self._set_control_code(wizard, invoice, data)

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
            invoice_id = self.env.context.get("invoice_id")
            invoice = self.env["account.invoice"].browse(invoice_id)
            wizard = self.env[active_model].browse(self.env.context.get('active_id'))

            data = {}
            data["form"] = invoice.read()[0]
            data["form"].update(
                wizard.read(
                    ['information_company_id', 'company_vat', 'company_city',
                    'company_street', 'company_street2', 'company_website',
                    'partner_id', 'partner_name', 'partner_vat', 'partner_city', 'partner_street',
                    'partner_street2', 'partner_website', 'state'
                    ])[0])

            self._set_date_literal(data)
            self._set_control_code(wizard, invoice, data)

            docargs = {
                'doc_ids': [invoice.id],
                'doc_model': "account.invoice",
                'data': data['form'],
                'docs': invoice,
                'time': time,
                'res_company_wizard': self.env['res.company'].browse(data['form']['information_company_id'][0]),
            }
            return self.env['report'].render('account_invoice_partner_wizard.report_invoices', docargs)
