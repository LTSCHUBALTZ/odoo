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
#
#    Developed by: thinkasoft , C.A.
#    Coded by: Aular Hector Manuel (aular.hector3@gmail.com)
#
##############################################################################

from openerp import models, fields, api


class AccountInvoicePartnerWizard(models.TransientModel):
    _inherit = "account.common.account.report"
    _name = 'account.invoice.partner.wizard'

    @api.model
    def _get_information_company_id(self):
        context = self.env.context
        invoice_obj = self.env["account.invoice"]
        if context.get("active_model", False) == "account.invoice":
            invoice_id = context.get("active_id", False)
            if invoice_id:
                invoice_rec = invoice_obj.browse(invoice_id)
                return invoice_rec.information_company_id
        return self.env["res.company"]

    @api.model
    def _get_partner_id(self):
        context = self.env.context
        invoice_obj = self.env["account.invoice"]
        if context.get("active_model", False) == "account.invoice":
            invoice_id = context.get("active_id", False)
            if invoice_id:
                invoice_rec = invoice_obj.browse(invoice_id)
                return invoice_rec.partner_id
        return self.env["res.partner"]

    def _get_state(self):
        context = self.env.context
        if context.get("active_model", False) == "account.invoice":
            if context.get("duplicate", False):
                return True
        return False


    information_company_id = fields.Many2one('res.company', required=True, string='Company', readonly=False, default=_get_information_company_id)
    company_vat = fields.Char(related='information_company_id.vat', string='TAX ID', readonly=True)
    company_city = fields.Char(related='information_company_id.city', string='City', readonly=True)
    company_street = fields.Char(related='information_company_id.street', string='Description', readonly=True)
    company_street2 = fields.Char(related='information_company_id.street2', string=' ', readonly=True)
    company_website = fields.Char(related='information_company_id.website', string=' ', readonly=True)

    partner_id = fields.Many2one('res.partner', required=True, string='Partner', readonly=True, default=_get_partner_id)
    partner_vat = fields.Char(related='partner_id.vat', string='TIN', readonly=True)
    partner_city = fields.Char(related='partner_id.city', string='City', readonly=True)
    partner_street = fields.Char(related='partner_id.street', string='Description', readonly=True)
    partner_street2 = fields.Char(related='partner_id.street2', string=' ', readonly=True)
    partner_website = fields.Char(related='partner_id.website', string=' ', readonly=True)
    state = fields.Boolean(string='Duplicate', default=_get_state, readonly=False, help="")

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data['form'].update(self.read(['information_company_id', 'company_vat', 'company_city', 'company_street', 'company_street2', 'company_website',
            'partner_id', 'partner_vat', 'partner_city', 'partner_street', 'partner_street2', 'partner_website','state'])[0])
        return self.env['report'].with_context(landscape=True).get_action(self, 'account_invoice_partner_wizard.report_invoices',data=data)
