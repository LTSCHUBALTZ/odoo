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


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    information_company_id = fields.Many2one("res.company", 
	string="Company", change_default=True,
        required=True, readonly=True, states={"draft": [("readonly", False)]},
        default=lambda self: self.env["res.company"]._company_default_get("account.invoice"))

    invoice_control_number = fields.Char(store=True, readonly=True, copy=False)

    @api.multi
    def invoice_validate(self):
        for invoice in self:
            invoice.invoice_control_number = invoice.information_company_id.sequence_id.next_by_id() 

        return super(AccountInvoice, self).invoice_validate()
