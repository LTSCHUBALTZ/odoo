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
from openerp.exceptions import Warning
from openerp.tools.translate import _
from openerp.exceptions import UserError


class AccountInvoicePartnerWizard(models.TransientModel):
    _name = 'account.invoice.partner.wizard'
    _inherit = ['mail.thread']

    @api.model
    def _get_information_company_id(self):
        context = self.env.context
        invoice_obj = self.env["account.invoice"]
        if context.get("active_model", False) == "account.invoice":
            invoice_id = context.get("active_id", False)
            if invoice_id:
                invoice_rec = invoice_obj.browse(invoice_id)
                if invoice_rec.printed:
                    return invoice_rec.wizard_information_company_id
                else:
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
                if invoice_rec.printed:
                    return invoice_rec.wizard_partner_id
                else:
                    return invoice_rec.partner_id
        return self.env["res.partner"]

    def _get_state(self):
        context = self.env.context
        if context.get("active_model", False) == "account.invoice":
            if context.get("duplicate", False):
                return True
        return False

    @api.model
    def _get_printed(self):
        context = self.env.context
        invoice_obj = self.env["account.invoice"]
        if context.get("active_model", False) == "account.invoice":
            invoice_id = context.get("active_id", False)
            if invoice_id:
                invoice_rec = invoice_obj.browse(invoice_id)
                return invoice_rec.printed
        return False

    @api.model
    def _get_company_authorization(self):
        context = self.env.context
        invoice_obj = self.env["account.invoice"]
        if context.get("active_model", False) == "account.invoice":
            invoice_id = context.get("active_id", False)
            if invoice_id:
                invoice_rec = invoice_obj.browse(invoice_id)
                if invoice_rec.printed:
                    return invoice_rec.wizard_company_authorization
                else:
                    return invoice_rec.information_company_id.authorization_num
        return False

    printed = fields.Boolean(default=_get_printed,
                             string='The invoice was printed or not')

    information_company_id = fields.Many2one('res.company', required=True, string='Company', readonly=False,
                                             default=_get_information_company_id)
    company_vat = fields.Char(related='information_company_id.vat', string='TAX ID', readonly=True)
    company_city = fields.Char(related='information_company_id.city', string='City', readonly=True)
    company_street = fields.Char(related='information_company_id.street', string='Description', readonly=True)
    company_street2 = fields.Char(related='information_company_id.street2', string=' ', readonly=True)
    company_website = fields.Char(related='information_company_id.website', string=' ', readonly=True)
    company_authorization = fields.Char(default=_get_company_authorization, size=20,
                                        string='Authorization Num')

    partner_id = fields.Many2one('res.partner', required=True, string='Partner', default=_get_partner_id)
    partner_name = fields.Char()
    partner_vat = fields.Char()
    partner_city = fields.Char(related='partner_id.city', string='City', readonly=True)
    partner_street = fields.Char(related='partner_id.street', string='Description', readonly=True)
    partner_street2 = fields.Char(related='partner_id.street2', string=' ', readonly=True)
    partner_website = fields.Char(related='partner_id.website', string=' ', readonly=True)
    state = fields.Boolean(string='Duplicate', default=_get_state, readonly=False, help="")

    @api.model
    def check_invoice_printed(self, invoice):
        if invoice.printed and not self.printed:
            raise Warning(_("This wizard should be closed. If you want print again, "
                            "close this windows and open again."))
        return True

    @api.model
    def save_data_of_wizard(self, invoice):
        if self.check_invoice_printed(invoice):
            if not invoice.printed:
                data = self.read()[0]
                invoice.write(
                    {
                        "printed": True,
                        "wizard_information_company_id": data.get("information_company_id")[0],
                        "wizard_company_authorization": data.get("company_authorization"),
                        "wizard_partner_id": data.get("partner_id")[0],
                        "wizard_partner_name": data.get("partner_name"),
                        "wizard_partner_vat": data.get("partner_vat"),
                    })
            return True
        return False

    @api.multi
    def print_report(self):
        context = self.env.context
        invoice_obj = self.env["account.invoice"]
        if context.get("active_model", False) == "account.invoice":
            invoice_id = context.get("active_id", False)
            if invoice_id:
                invoice = invoice_obj.browse(invoice_id)

        if not invoice.invoice_control_number:
            raise UserError(_('Please Generate Invoice control number.'))
        if self.save_data_of_wizard(invoice):
            self._compute_partner_vat()
            data = {}
            data_dict = invoice.read()[0]
            data["form"] = data_dict
            data["form"].update(
                self.read(
                    ['information_company_id', 'company_vat', 'company_city',
                     'company_street', 'company_street2', 'company_website',
                     'partner_id', 'partner_name', 'partner_vat',
                     'partner_city', 'partner_street',
                     'partner_street2', 'partner_website', 'state'
                     ])[0])
            return self.env['report'].get_action(
                self, 'account_invoice_partner_wizard.report_invoices',
                data=data)

    @api.onchange('partner_id')
    def _compute_partner_vat(self):
        context = self.env.context
        invoice_obj = self.env["account.invoice"]
        for partner in self:
            if context.get("active_model", False) == "account.invoice":
                invoice_id = context.get("active_id", False)
                if invoice_id:
                    invoice = invoice_obj.browse(invoice_id)
            if invoice and invoice.printed:
                partner.partner_vat = invoice.wizard_partner_vat
                partner.partner_name = invoice.wizard_partner_name
            else:
                partner.partner_vat = partner.partner_id.vat
                partner.partner_name = partner.partner_id.name

    @api.multi
    def action_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref('account_invoice_partner_wizard.email_template_edi_invoice_partner', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        invoice_id = self.env.context.get("active_id")

        invoice_obj = self.env["account.invoice"]
        if invoice_id:
            invoice = invoice_obj.browse(invoice_id)
        self.check_invoice_printed(invoice)

        ctx = dict(
            default_model='account.invoice.partner.wizard',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            invoice_id=invoice_id,
        )

        return {
            'name': 'Compose Email',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }


class MailComposer(models.TransientModel):

    _inherit = 'mail.compose.message'

    @api.multi
    def send_mail_action(self):
        context = self._context
        invoice_id = context.get("invoice_id", False)
        if invoice_id and \
                context.get(
                    "active_model", False) == "account.invoice.partner.wizard":
            account_obj = self.env["account.invoice"]
            wizard_obj = self.env["account.invoice.partner.wizard"]
            invoice = account_obj.browse(invoice_id)
            invoice.write({'email_sent': True})
            wizard = wizard_obj.browse(context.get("active_id"))

        if wizard.save_data_of_wizard(invoice):
            res = super(MailComposer, self).send_mail_action()
            return res
