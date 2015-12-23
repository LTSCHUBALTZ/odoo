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
    _inherit = 'account.invoice'

    vat = fields.Char(related='company_id.vat', string='TAX ID', readonly=True)
    city = fields.Char(related='company_id.city', string='City', readonly=True)
    street = fields.Char(related='company_id.street', string='Description', readonly=True)
    street2 = fields.Char(related='company_id.street2', string=' ', readonly=True)
    website = fields.Char(related='company_id.website', string=' ', readonly=True)
    nro_authorization = fields.Integer(related='company_id.nro_authorization', string='Nro. Authorization', readonly=True)
    nro_init = fields.Integer(related='company_id.nro_init', string='Start Number', readonly=True)
    nro_final = fields.Integer(related='company_id.nro_final', string='Final Number', readonly=True)
    issuance_deadline = fields.Date(related='company_id.issuance_deadline', string='Issuance Deadline', readonly=True)
    account_key = fields.Char(related='company_id.account_key', string='Key', readonly=True)
    footer = fields.Char(related='company_id.footer', string='footer', readonly=True)
