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
import oso


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    information_company_id = fields.Many2one("res.company", 
	string="Company", change_default=True,
        required=True, readonly=True, states={"draft": [("readonly", False)]},
        default=lambda self: self.env["res.company"]._company_default_get("account.invoice"))
    vat = fields.Char(related="information_company_id.vat", string="TAX ID", readonly=True)
    city = fields.Char(related="information_company_id.city", string="City", readonly=True)
    street = fields.Char(related="information_company_id.street", string="Description", readonly=True)
    street2 = fields.Char(related="information_company_id.street2", string=" ", readonly=True)
    website = fields.Char(related="information_company_id.website", string=" ", readonly=True)
    authorization_num = fields.Integer(related="information_company_id.authorization_num", string="Authorization Number", readonly=True)
    init_num = fields.Integer(related="information_company_id.init_num", string="Start Number", readonly=True)
    final_num = fields.Integer(related="information_company_id.final_num", string="Final Number", readonly=True)
    issuance_deadline = fields.Date(related="information_company_id.issuance_deadline", string="Issuance Deadline", readonly=True)
    account_key = fields.Char(related="information_company_id.account_key", string="Key", readonly=True)
    control_code = fields.Char(compute="_get_control_code", string="Control Code", readonly=True)

    @api.depends("vat")
    def _get_control_code(self):
        for invoice in self:
            qr = oso.CodigoControlV7()
            invoice.control_code = qr.generar(self.authorization_num, 32423, 1665979, 20080519, 35959, "zZ7Z]xssKqkEf_6K9uH(EcV+%x+u[Cca9T%+_$kiLjT8(zr3T9b5Fx2xG-D+_EBS")
            # invoice.control_code = qr.generar(self.authorization_num, self.number, self.partner_id.vat, self.date_invoice, self.amount_total, self.information_company_id.account_key)
