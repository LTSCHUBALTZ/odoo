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
import amount_to_text_es_BOL


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    amount_to_text = fields.Char(compute="_compute_amount_to_text", size=256, string='Amount to Text', help='Amount of the invoice in letter')

    @api.depends('amount_total')
    def _compute_amount_to_text(self):
        if self.amount_total > 0:
            for invoice in self:
                invoice.amount_to_text = amount_to_text_es_BOL.get_amount_to_text(self, invoice.amount_total, 'es_cheque', invoice.currency_id.name)
