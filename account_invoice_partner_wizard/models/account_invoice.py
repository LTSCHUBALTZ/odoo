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
from datetime import datetime
import oso


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    vat = fields.Char(related="information_company_id.vat", string="TAX ID", readonly=True)
    city = fields.Char(related="information_company_id.city", string="City", readonly=True)
    street = fields.Char(related="information_company_id.street", string="Description", readonly=True)
    street2 = fields.Char(related="information_company_id.street2", string=" ", readonly=True)
    website = fields.Char(related="information_company_id.website", string=" ", readonly=True)
    authorization_num = fields.Integer(related="information_company_id.authorization_num", string="Authorization Number", readonly=True)
    final_num = fields.Integer(related="information_company_id.final_num", string="Final Number", readonly=True)
    issuance_deadline = fields.Date(related="information_company_id.issuance_deadline", string="Issuance Deadline", readonly=True)
    account_key = fields.Char(related="information_company_id.account_key", string="Key", readonly=True)
    control_code = fields.Char(compute="_compute_control_code", string="Control Code", readonly=True, store=True)
    check_report = fields.Boolean(string="check_report", default=True, copy=False)

    @api.depends('date_invoice', 'invoice_control_number')
    def _compute_control_code(self):
        for invoice in self:
            if invoice.date_invoice and invoice.invoice_control_number:
                invoice_control_number = "".join([x for x in invoice.invoice_control_number if x.isdigit()])
                vat = "".join([x for x in invoice.partner_id.vat if x.isdigit()]) if invoice.partner_id.vat else 0
                date_invoice = "".join([x for x in invoice.date_invoice if x.isdigit()])
                qr = oso.CodigoControlV7()
                control_code = qr.generar(invoice.authorization_num, int(invoice_control_number), int(vat), int(date_invoice), int(invoice.amount_total), invoice.information_company_id.account_key)
                invoice.control_code = "%s|%s|%s|%s|%s|0|%s|%s|0|0|0|0" % (
                    invoice.vat,
                    invoice.invoice_control_number,
                    invoice.authorization_num,
                    datetime.strptime(invoice.date_invoice, '%Y-%m-%d').strftime('%m/%d/%Y'),
                    invoice.amount_total,
                    control_code,
                    invoice.partner_id.vat,
                )

    @api.onchange('authorization_num')
    def _verify_authorization_num(self):
        for invoice in self:
            if not invoice.authorization_num:
                return {
                    'warning': {
                        'title': "Incorrect 'Authorization Number' value",
                        'message': "The record is empty, check the settings of the company",
                    }
                }

    @api.onchange('vat')
    def _verify_vat(self):
        for invoice in self:
            if invoice.vat:
                check_vat = "".join([x for x in self.vat if x.isdigit()]) if self.vat else False
                if check_vat.isalpha():
                    return {
                        'warning': {
                            'title': "Incorrect 'Vat' value",
                            'message': "The record is formatted incorrectly",
                        }
                    }
            else:
                return {
                    'warning': {
                        'title': "Incorrect 'Vat' value",
                        'message': "The record is empty",
                    }
                }

    @api.onchange('account_key')
    def _verify_account_key(self):
        for invoice in self:
            if not invoice.account_key:
                return {
                    'warning': {
                        'title': "Incorrect 'Key' value",
                        'message': "The record  is empty, check the settings of the company in the field Key",
                    }
                }

    @api.multi
    def action_invoice_partner_wizard(self):
        self.ensure_one()
        self.write({'check_report': True})
        compose_form = self.env.ref(
            'account_invoice_partner_wizard.account_invoice_partner_wizard_form',
            False
        )
        ctx = dict(
            print_report=True,
        )
        return {
            'name': 'Invoices QR',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.invoice.partner.wizard',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }
