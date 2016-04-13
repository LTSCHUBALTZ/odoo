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
    authorization_num = fields.Char(related="information_company_id.authorization_num", size=20,
                                    string="Authorization Number", readonly=True)
    final_num = fields.Integer(related="information_company_id.final_num", string="Final Number", readonly=True)
    issuance_deadline = fields.Date(related="information_company_id.issuance_deadline",
                                    string="Issuance Deadline", readonly=True)
    account_key = fields.Char(related="information_company_id.account_key", string="Key", readonly=True)
    control_code = fields.Char(compute="_compute_control_code", string="Control Code", readonly=True, store=True)
    printed = fields.Boolean(string="The invoice was printed or not", default=False, copy=False)
    email_sent = fields.Boolean(string="The invoice was sent or not", default=False, copy=False)

    wizard_information_company_id = fields.Many2one('res.company', string='Company')
    wizard_company_authorization = fields.Char(string='Authorization Num', size=20)
    wizard_partner_id = fields.Many2one('res.partner', string='Partner')
    wizard_partner_name = fields.Char()
    wizard_partner_vat = fields.Char()

    @api.model
    def _get_control_code(self, company_id, partner_id, authorization_num=False):
        """ Crear un codigo especial de la compañia. Un ejemplo: 55-99-F4-97
        """
        # Si no se manda un numero de autorizacion, se utiliza el
        # numero de autorizacion de la compañia
        # Cuando no se manda el numero de autorizacion es porque se esta
        # calculado el codigo para el codigo de control de la factura
        if not authorization_num:
            authorization_num = company_id.authorization_num
        invoice_control_number = "".join([x for x in self.invoice_control_number if x.isdigit()])
        vat = "".join([x for x in partner_id.vat if x.isdigit()]) if partner_id.vat else 0
        date_invoice = "".join([x for x in self.date_invoice if x.isdigit()])
        qr = oso.CodigoControlV7()
        control_code = qr.generar(authorization_num, int(invoice_control_number),
                                  int(vat), int(date_invoice),
                                  int(round(self.amount_total)),
                                  company_id.account_key)
        return control_code

    @api.model
    def _get_control_code_final(self, control_code, company_id, vat_partner, authorization_num=False):
        """ La finalidad de este metodo es crear un codigo de control para la
        factura. Cuando el codigo QR es escaneado, la informacion mostrada es
        el codigo de control que se retorna en este metodo. El codigo de
        control se forma utilizando los parametros recibidos por el método y
        datos de la factura.
        Ejemplo que pueda retornar:
        1234|00004|423423542|08/04/2016|750.0|0|55-99-F4-97|False|0|0|0|0
        """
        # Si no se manda un numero de autorizacion, se utiliza el
        # numero de autorizacion de la compañia, esto es para el campo
        # de la factura.
        # Cuando se especifica un numero de autorizacion es porque el
        # metodo es llamado desde la impresion del reporte, y el código
        # de control es distinto al de la factura
        if not authorization_num:
            authorization_num = company_id.authorization_num

        control_code_final = "%s|%s|%s|%s|%s|0|%s|%s|0|0|0|0" % (
            company_id.partner_id.vat,
            self.invoice_control_number,
            authorization_num,
            datetime.strptime(self.date_invoice, '%Y-%m-%d').strftime('%d/%m/%Y'),
            self.amount_total,
            control_code,
            vat_partner,
        )
        return control_code_final

    @api.depends('date_invoice', 'invoice_control_number')
    def _compute_control_code(self):
        """ Re-calcular el codigo de control si algunos de los
        campos arriba cambia.
        """
        for invoice in self:
            if invoice.date_invoice and invoice.invoice_control_number:
                control_code = invoice._get_control_code(
                    invoice.information_company_id,
                    invoice.partner_id)
                invoice.control_code = invoice._get_control_code_final(
                    control_code,
                    invoice.information_company_id,
                    invoice.partner_id.vat)

    @api.onchange('authorization_num')
    def _verify_authorization_num(self):
        """ Cuando se selecciona una compañia en la factura.
        La compañia debe tener los valores establecidos
        correctamente.
        La compañia debe tener establecido un numero de autorizacion
        obligatoriamente.
        """
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
        """ Cuando se selecciona una compañia en la factura.
        La compañia debe tener los valores establecidos
        correctamente.
        El vat de la empresa debe ser un numero entero
        obligatoriamente
        """
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
        """ Cuando se selecciona una compañia en la factura.
        La compañia debe tener los valores establecidos
        correctamente.
        La compañía debe tener establecido un account_key
        obligatoriamente.
        """
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
